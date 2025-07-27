#!/usr/bin/env python3
"""
Views for the messaging application.

This module contains Django REST Framework viewsets for handling
conversations and messages with proper API endpoints and filtering.
"""

from rest_framework import viewsets, status, permissions, filters, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from .models import User, Conversation, Message
from .serializers import (
    UserSerializer,
    ConversationSerializer,
    ConversationCreateSerializer,
    ConversationDetailSerializer,
    MessageSerializer,
    MessageCreateSerializer
)
from .permissions import IsParticipantOfConversation, IsMessageSender, IsOwnerOrReadOnly, IsAdminOrReadOnly
from .filters import MessageFilter, ConversationFilter
from .pagination import MessagePagination, ConversationPagination, UserPagination


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model operations.
    
    Provides CRUD operations for user management with proper
    permissions and validation.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    pagination_class = UserPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['role', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['created_at', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    
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
    and managing conversation participants with nested message relationships.
    """
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation]
    pagination_class = ConversationPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ['participants_id__email', 'participants_id__first_name', 'participants_id__last_name']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Return conversations where the current user is a participant."""
        user = self.request.user
        return Conversation.objects.filter(
            participants_id=user
        ).prefetch_related(
            Prefetch(
                'participants_id',
                queryset=User.objects.only('id', 'email', 'first_name', 'last_name', 'role')
            ),
            Prefetch(
                'messages',
                queryset=Message.objects.select_related('sender_id').order_by('-sent_at')
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
        """Create conversation with current user as participant."""
        conversation = serializer.save()
        return conversation
    
    @action(detail=True, methods=['get'])
    def participant(self, request, pk=None):
        """Get participant information in a conversation."""
        conversation = self.get_object()
        participant = conversation.participants_id
        serializer = UserSerializer(participant)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message model operations.
    
    Provides endpoints for listing messages, sending new messages,
    and managing message content with support for nested routing.
    """
    permission_classes = [permissions.IsAuthenticated, IsParticipantOfConversation, IsMessageSender]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ['message_body', 'sender_id__email', 'sender_id__first_name', 'sender_id__last_name']
    ordering_fields = ['sent_at', 'sender_id__first_name', 'sender_id__last_name']
    ordering = ['-sent_at']
    
    def get_queryset(self):
        """Return messages based on context (nested or standalone)."""
        user = self.request.user
        
        # Check if we're in a nested route (conversation messages)
        conversation_pk = self.kwargs.get('conversation_pk')
        if conversation_pk:
            # Nested route: return messages for specific conversation
            return Message.objects.filter(
                sender_id=user,
                conversation_id=conversation_pk
            ).select_related('sender_id').order_by('-sent_at')
        else:
            # Standalone route: return all messages sent by user
            return Message.objects.filter(
                sender_id=user
            ).select_related('sender_id').order_by('-sent_at')
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['create', 'send_message']:
            return MessageCreateSerializer
        return MessageSerializer
    
    def perform_create(self, serializer):
        """Create message with current user as sender."""
        # Check if we're in a nested route and set conversation
        conversation_pk = self.kwargs.get('conversation_pk')
        if conversation_pk:
            try:
                conversation = Conversation.objects.get(conversation_id=conversation_pk)
                serializer.save(sender_id=self.request.user, conversation=conversation)
            except Conversation.DoesNotExist:
                raise serializers.ValidationError("Conversation not found.")
        else:
            serializer.save(sender_id=self.request.user)
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """Send a message."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check if we're in a nested route and set conversation
            conversation_pk = self.kwargs.get('conversation_pk')
            if conversation_pk:
                try:
                    conversation = Conversation.objects.get(conversation_id=conversation_pk)
                    message = serializer.save(sender_id=request.user, conversation=conversation)
                except Conversation.DoesNotExist:
                    return Response(
                        {'error': 'Conversation not found'}, 
                        status=status.HTTP_404_NOT_FOUND
                    )
            else:
                message = serializer.save(sender_id=request.user)
            
            # Return the created message with full details
            response_serializer = MessageSerializer(message)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def my_messages(self, request):
        """Get messages sent by the current user."""
        user = request.user
        messages = self.get_queryset()
        
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
        
        messages = self.get_queryset().filter(
            message_body__icontains=query
        )
        
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
        if message.sender_id != request.user:
            return Response(
                {'error': 'You can only edit your own messages'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Delete message - only allow sender to delete their own messages."""
        message = self.get_object()
        
        # Only the sender can delete their own messages
        if message.sender_id != request.user:
            return Response(
                {'error': 'You can only delete your own messages'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        return super().destroy(request, *args, **kwargs)
