#!/usr/bin/env python3
"""
Models for the messaging application.

This module defines the data models for conversations and messages
according to the specified database schema.
"""

import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Conversation(models.Model):
    """
    Conversation model to track which users are involved in a conversation.
    
    This model represents a conversation between users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    participants_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='conversations',
        db_column='participants_id',
        null=True,  # Temporarily allow null for migration
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'conversation'
        indexes = [
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"Conversation {self.conversation_id}"


class Message(models.Model):
    """
    Message model containing the sender, conversation, and message content.
    
    This model represents individual messages within a conversation.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sender_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_messages',
        db_column='sender_id'
    )
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        null=True,
        blank=True
    )
    message_body = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'message'
        indexes = [
            models.Index(fields=['sent_at']),
            models.Index(fields=['conversation', 'sent_at']),
        ]
        ordering = ['sent_at']
    
    def __str__(self):
        return f"Message from {self.sender_id} at {self.sent_at}"
