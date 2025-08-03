#!/usr/bin/env python3
"""
Custom permissions for the messaging application.

This module defines custom permission classes to control access
to conversations and messages based on user participation.
"""

from rest_framework import permissions
from .models import Conversation, Message


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation
    to access its messages and details.
    
    This permission ensures that users can only:
    - View conversations they are part of
    - Send messages to conversations they are part of
    - View messages in conversations they are part of
    - Update/delete their own messages in conversations they are part of
    """
    
    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the action.
        
        Args:
            request: The HTTP request object
            view: The view being accessed
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Allow all authenticated users to create conversations
        if request.method == 'POST' and view.action == 'create':
            return request.user.is_authenticated
        
        # Allow authenticated users to list conversations
        if request.method == 'GET' and view.action == 'list':
            return request.user.is_authenticated
        
        return True
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access a specific object.
        
        Args:
            request: The HTTP request object
            view: The view being accessed
            obj: The object being accessed (Conversation or Message)
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # Handle Conversation objects
        if isinstance(obj, Conversation):
            return self._check_conversation_permission(request, obj)
        
        # Handle Message objects
        elif isinstance(obj, Message):
            return self._check_message_permission(request, obj)
        
        return False
    
    def _check_conversation_permission(self, request, conversation):
        """
        Check if user has permission to access a conversation.
        
        Args:
            request: The HTTP request object
            conversation: The conversation object
            
        Returns:
            bool: True if user is a participant, False otherwise
        """
        # User must be a participant of the conversation
        return conversation.participants_id == request.user
    
    def _check_message_permission(self, request, message):
        """
        Check if user has permission to access a message.
        
        Args:
            request: The HTTP request object
            message: The message object
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # User must be a participant of the conversation
        if not self._check_conversation_permission(request, message.conversation):
            return False
        
        # For update/delete operations, user must be the sender
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return message.sender_id == request.user
        
        # For read operations, user just needs to be a participant
        return True


class IsMessageSender(permissions.BasePermission):
    """
    Custom permission to allow only the sender of a message
    to update or delete it.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the sender of the message.
        
        Args:
            request: The HTTP request object
            view: The view being accessed
            obj: The message object
            
        Returns:
            bool: True if user is the sender, False otherwise
        """
        # Ensure user is authenticated
        if not request.user.is_authenticated:
            return False
        
        # For update/delete operations, user must be the sender
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return obj.sender_id == request.user
        
        # For read operations, check conversation participation
        return IsParticipantOfConversation().has_object_permission(request, view, obj)


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of an object
    to modify it, while allowing read access to all authenticated users.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user is the owner of the object.
        
        Args:
            request: The HTTP request object
            view: The view being accessed
            obj: The object being accessed
            
        Returns:
            bool: True if user is the owner or method is safe, False otherwise
        """
        # Read permissions are allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions are only allowed to the owner
        return obj.id == request.user.id


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admin users to modify objects,
    while allowing read access to all authenticated users.
    """
    
    def has_permission(self, request, view):
        """
        Check if the user has permission to perform the action.
        
        Args:
            request: The HTTP request object
            view: The view being accessed
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Read permissions are allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions are only allowed to admin users
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.is_superuser or 
            request.user.role == 'admin'
        )
    
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access a specific object.
        
        Args:
            request: The HTTP request object
            view: The view being accessed
            obj: The object being accessed
            
        Returns:
            bool: True if user has permission, False otherwise
        """
        # Read permissions are allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions are only allowed to admin users
        return request.user.is_authenticated and (
            request.user.is_staff or 
            request.user.is_superuser or 
            request.user.role == 'admin'
        ) 