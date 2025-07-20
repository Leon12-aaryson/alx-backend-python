#!/usr/bin/env python3
"""
Models for the messaging application.

This module defines the data models for users, conversations, and messages
according to the specified database schema.
"""

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    
    Additional fields for user profile information and role management.
    """
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    
    # Primary key as specified in the database schema
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Override username to use email
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    
    # Password hash field as specified in the database schema
    password_hash = models.CharField(max_length=128, verbose_name='password_hash')
    
    # Additional fields
    first_name = models.CharField(max_length=150, null=False, blank=False)
    last_name = models.CharField(max_length=150, null=False, blank=False)
    phone_number = models.CharField(
        max_length=15, 
        null=True, 
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='guest',
        null=False,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Use email as the username field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']
    
    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
        ]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"


class Conversation(models.Model):
    """
    Conversation model to track which users are involved in a conversation.
    
    This model represents a conversation between users.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations',
        db_column='participants_id'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'conversation'
        indexes = [
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Conversation {self.conversation_id} with {self.participants_id.first_name}"


class Message(models.Model):
    """
    Message model containing the sender, conversation, and message content.
    
    This model represents individual messages within a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        db_column='sender_id'
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message'
        indexes = [
            models.Index(fields=['sent_at']),
        ]
        ordering = ['sent_at']
    
    def __str__(self):
        return f"Message {self.message_id} from {self.sender_id.first_name} at {self.sent_at}"
