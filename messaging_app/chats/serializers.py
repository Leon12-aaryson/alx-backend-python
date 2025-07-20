#!/usr/bin/env python3
"""
Serializers for the messaging application.

This module contains Django REST Framework serializers for the User,
Conversation, and Message models with proper handling of relationships.
"""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    
    Handles user data serialization and deserialization with proper
    field validation and security considerations.
    """
    first_name = serializers.CharField(max_length=150, required=True)
    last_name = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=True)
    phone_number = serializers.CharField(max_length=15, required=False, allow_blank=True)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    
    class Meta:
        model = User
        fields = [
            'user_id', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'created_at', 'is_active'
        ]
        read_only_fields = ['user_id', 'created_at']
        extra_kwargs = {
            'password_hash': {'write_only': True},
        }
    
    def create(self, validated_data):
        """Create a new user with proper password hashing."""
        password = validated_data.pop('password_hash', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update user with proper password handling."""
        password = validated_data.pop('password_hash', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class UserSummarySerializer(serializers.ModelSerializer):
    """
    Simplified user serializer for nested relationships.
    
    Used when including user information within other serializers
    to avoid circular dependencies and reduce payload size.
    """
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['user_id']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    
    Includes sender information and handles message creation
    with proper validation.
    """
    sender_id = UserSummarySerializer(read_only=True, source='sender_id')
    sender_id_input = serializers.UUIDField(write_only=True, source='sender_id')
    message_body = serializers.CharField(required=True, allow_blank=False)
    
    class Meta:
        model = Message
        fields = [
            'message_id', 'sender_id', 'sender_id_input', 
            'message_body', 'sent_at'
        ]
        read_only_fields = ['message_id', 'sent_at', 'sender_id']
    
    def validate_sender_id_input(self, value):
        """Validate that the sender_id corresponds to an existing user."""
        try:
            User.objects.get(user_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return value
    
    def validate_message_body(self, value):
        """Validate that message body is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value
    
    def create(self, validated_data):
        """Create a message with proper sender assignment."""
        sender_id = validated_data.pop('sender_id')
        sender = User.objects.get(user_id=sender_id)
        message = Message.objects.create(sender_id=sender, **validated_data)
        return message


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    
    Includes participant information with proper relationships.
    """
    participants_id = UserSummarySerializer(read_only=True)
    participant_id_input = serializers.UUIDField(write_only=True, source='participants_id')
    
    class Meta:
        model = Conversation
        fields = [
            'conversation_id', 'participants_id', 'participant_id_input', 'created_at'
        ]
        read_only_fields = ['conversation_id', 'created_at', 'participants_id']
    
    def validate_participant_id_input(self, value):
        """Validate that the participant_id corresponds to an existing user."""
        try:
            User.objects.get(user_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return value
    
    def create(self, validated_data):
        """Create a conversation with participant assignment."""
        participant_id = validated_data.pop('participants_id')
        participant = User.objects.get(user_id=participant_id)
        conversation = Conversation.objects.create(participants_id=participant, **validated_data)
        return conversation


class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new conversations.
    
    Handles participant assignment during conversation creation.
    """
    participant_id = serializers.UUIDField(write_only=True, required=True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participant_id', 'created_at']
        read_only_fields = ['conversation_id', 'created_at']
    
    def validate_participant_id(self, value):
        """Validate that the participant ID corresponds to an existing user."""
        try:
            User.objects.get(user_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return value
    
    def create(self, validated_data):
        """Create a conversation and assign participant."""
        participant_id = validated_data.pop('participant_id')
        participant = User.objects.get(user_id=participant_id)
        conversation = Conversation.objects.create(participants_id=participant, **validated_data)
        return conversation


class ConversationDetailSerializer(ConversationSerializer):
    """
    Detailed conversation serializer.
    
    Used for retrieving complete conversation details.
    """
    class Meta(ConversationSerializer.Meta):
        fields = [
            'conversation_id', 'participants_id', 'participant_id_input', 'created_at'
        ]


class MessageCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new messages.
    
    Simplified serializer for message creation without nested data.
    """
    sender_id = serializers.UUIDField(write_only=True)
    message_body = serializers.CharField(required=True, allow_blank=False)
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body', 'sent_at']
        read_only_fields = ['message_id', 'sent_at']
    
    def validate_sender_id(self, value):
        """Validate that the sender_id corresponds to an existing user."""
        try:
            User.objects.get(user_id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return value
    
    def validate_message_body(self, value):
        """Validate that message body is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value
    
    def validate(self, data):
        """Additional validation for message creation."""
        if not data.get('message_body'):
            raise serializers.ValidationError("Message body is required.")
        return data
    
    def create(self, validated_data):
        """Create a message with proper sender assignment."""
        sender_id = validated_data.pop('sender_id')
        sender = User.objects.get(user_id=sender_id)
        message = Message.objects.create(sender_id=sender, **validated_data)
        return message 