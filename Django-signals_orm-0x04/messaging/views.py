from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Q, Prefetch
from .models import Message, Notification, Conversation
from .serializers import UserSerializer, MessageSerializer, NotificationSerializer, ConversationSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for User model."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['delete'])
    def delete_user(self, request, pk=None):
        """
        Delete user account and all related data.
        This will trigger the post_delete signal to clean up related data.
        """
        user = self.get_object()
        
        # Check if user is trying to delete themselves
        if user != request.user:
            return Response(
                {"error": "You can only delete your own account"}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Delete the user (this will trigger the post_delete signal)
        user.delete()
        
        return Response(
            {"message": "User account deleted successfully"}, 
            status=status.HTTP_204_NO_CONTENT
        )


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for Message model with advanced ORM techniques."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Optimize queries with select_related and prefetch_related."""
        return Message.objects.select_related('sender', 'receiver', 'parent_message').prefetch_related(
            'replies__sender',
            'replies__receiver'
        )

    @method_decorator(cache_page(60))  # Cache for 60 seconds
    @action(detail=False, methods=['get'])
    def conversation_messages(self, request):
        """
        Cached view to display messages in a conversation.
        Uses cache_page decorator for 60 seconds cache timeout.
        """
        conversation_id = request.query_params.get('conversation_id')
        if not conversation_id:
            return Response(
                {"error": "conversation_id parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        messages = Message.objects.filter(
            conversation__conversation_id=conversation_id
        ).select_related('sender', 'receiver').prefetch_related('replies')
        
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def unread_messages(self, request):
        """
        Get unread messages for the current user using custom manager.
        """
        unread_messages = Message.unread.unread_for_user(request.user)
        serializer = self.get_serializer(unread_messages, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def threaded_conversation(self, request):
        """
        Get threaded conversation with all replies using advanced ORM techniques.
        """
        message_id = request.query_params.get('message_id')
        if not message_id:
            return Response(
                {"error": "message_id parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the main message and all its replies recursively
        main_message = Message.objects.select_related('sender', 'receiver').get(id=message_id)
        
        # Get all replies using prefetch_related for optimization
        replies = Message.objects.filter(
            parent_message=main_message
        ).select_related('sender', 'receiver').prefetch_related(
            'replies__sender',
            'replies__receiver'
        )
        
        # Build threaded structure
        threaded_data = {
            'main_message': MessageSerializer(main_message).data,
            'replies': MessageSerializer(replies, many=True).data
        }
        
        return Response(threaded_data)

    @action(detail=True, methods=['post'])
    def reply_to_message(self, request, pk=None):
        """
        Create a reply to a specific message (threaded conversation).
        """
        parent_message = self.get_object()
        content = request.data.get('content')
        
        if not content:
            return Response(
                {"error": "content is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create reply message
        reply = Message.objects.create(
            sender=request.user,
            receiver=parent_message.sender,  # Reply to the sender of the original message
            content=content,
            parent_message=parent_message
        )
        
        serializer = self.get_serializer(reply)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class NotificationViewSet(viewsets.ModelViewSet):
    """ViewSet for Notification model."""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter notifications for the current user."""
        return Notification.objects.filter(user=self.request.user).select_related('message', 'user')


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for Conversation model."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Optimize conversation queries."""
        return Conversation.objects.prefetch_related(
            'participants',
            'messages__sender',
            'messages__receiver'
        )

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """
        Get all messages in a conversation with threading support.
        """
        conversation = self.get_object()
        messages = Message.objects.filter(
            conversation=conversation
        ).select_related('sender', 'receiver').prefetch_related(
            'replies__sender',
            'replies__receiver'
        )
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
