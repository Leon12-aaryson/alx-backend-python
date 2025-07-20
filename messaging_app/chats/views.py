#!/usr/bin/env python3
"""
Views for the messaging application.

This module contains Django REST Framework viewsets for handling
conversations and messages with proper API endpoints.
"""

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Prefetch
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    ConversationCreateSerializer,
    ConversationDetailSerializer,
    MessageSerializer,
    MessageCreateSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model operations.
    
    Provides CRUD operations for user management with proper
    permissions and validation.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return users based on current user's permissions."""
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['create', 'update', 'partial_update']:
            return UserSerializer
        return UserSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversation model operations.
    
    Provides endpoints for listing conversations, creating new ones,
    and managing conversation participants.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return conversations where the current user is a participant."""
        user = self.request.user
        return Conversation.objects.filter(
            participants=user
        ).prefetch_related(
            Prefetch(
                'participants',
                queryset=User.objects.only('id', 'email', 'first_name', 'last_name', 'role')
            ),
            Prefetch(
                'messages',
                queryset=Message.objects.select_related('sender').order_by('-sent_at')
            )
        ).order_by('-created_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ConversationCreateSerializer
        elif self.action in ['retrieve', 'detail']:
            return ConversationDetailSerializer
        return ConversationSerializer
    
    def perform_create(self, serializer):
        """Create conversation and add current user as participant."""
        conversation = serializer.save()
        
        # Add current user as participant if not already included
        if not conversation.participants.filter(id=self.request.user.id).exists():
            conversation.participants.add(self.request.user)
        
        return conversation
    
    @action(detail=True, methods=['post'])
    def add_participant(self, request, pk=None):
        """Add a participant to an existing conversation."""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if conversation.participants.filter(id=user_id).exists():
            return Response(
                {'error': 'User is already a participant'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation.participants.add(user)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def remove_participant(self, request, pk=None):
        """Remove a participant from a conversation."""
        conversation = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not conversation.participants.filter(id=user_id).exists():
            return Response(
                {'error': 'User is not a participant'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Prevent removing the last participant
        if conversation.participants.count() <= 1:
            return Response(
                {'error': 'Cannot remove the last participant'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        conversation.participants.remove(user)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def participants(self, request, pk=None):
        """Get list of participants in a conversation."""
        conversation = self.get_object()
        participants = conversation.participants.all()
        serializer = UserSerializer(participants, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        """Get messages in a conversation with pagination."""
        conversation = self.get_object()
        messages = conversation.messages.select_related('sender').order_by('-sent_at')
        
        # Pagination
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message model operations.
    
    Provides endpoints for listing messages, sending new messages,
    and managing message content.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return messages from conversations where user is a participant."""
        user = self.request.user
        return Message.objects.filter(
            conversation__participants=user
        ).select_related('sender', 'conversation').order_by('-sent_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['create', 'send_message']:
            return MessageCreateSerializer
        return MessageSerializer
    
    def perform_create(self, serializer):
        """Create message with current user as sender."""
        serializer.save(sender=self.request.user)
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """Send a message to a conversation."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Set the sender to the current user
            message = serializer.save(sender=request.user)
            
            # Return the created message with full details
            response_serializer = MessageSerializer(message)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def conversation_messages(self, request, pk=None):
        """Get all messages from a specific conversation."""
        conversation_id = pk
        user = request.user
        
        # Verify user is participant in conversation
        try:
            conversation = Conversation.objects.get(
                id=conversation_id,
                participants=user
            )
        except Conversation.DoesNotExist:
            return Response(
                {'error': 'Conversation not found or access denied'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        messages = conversation.messages.select_related('sender').order_by('-sent_at')
        
        # Pagination
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_messages(self, request):
        """Get messages sent by the current user."""
        user = request.user
        messages = Message.objects.filter(
            sender=user
        ).select_related('conversation').order_by('-sent_at')
        
        # Pagination
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def search(self, request):
        """Search messages by content."""
        query = request.query_params.get('q', '')
        user = request.user
        
        if not query:
            return Response(
                {'error': 'Search query is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        messages = Message.objects.filter(
            conversation__participants=user,
            message_body__icontains=query
        ).select_related('sender', 'conversation').order_by('-sent_at')
        
        # Pagination
        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = MessageSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update message - only allow sender to update their own messages."""
        message = self.get_object()
        
        # Only the sender can update their own messages
        if message.sender != request.user:
            return Response(
                {'error': 'You can only edit your own messages'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Delete message - only allow sender to delete their own messages."""
        message = self.get_object()
        
        # Only the sender can delete their own messages
        if message.sender != request.user:
            return Response(
                {'error': 'You can only delete your own messages'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
