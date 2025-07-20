#!/usr/bin/env python3
"""
Serializers for the messaging application.

This module contains Django REST Framework serializers for the User,
Conversation, and Message models with proper handling of nested relationships.
"""

from rest_framework import serializers
from .models import User, Conversation, ConversationParticipant, Message


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
            'id', 'email', 'first_name', 'last_name', 
            'phone_number', 'role', 'created_at', 'is_active'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        """Create a new user with proper password hashing."""
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
    
    def update(self, instance, validated_data):
        """Update user with proper password handling."""
        password = validated_data.pop('password', None)
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
        fields = ['id', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    
    Includes sender information and handles message creation
    with proper validation.
    """
    sender = UserSummarySerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True)
    message_body = serializers.CharField(required=True, allow_blank=False)
    
    class Meta:
        model = Message
        fields = [
            'id', 'sender', 'sender_id', 'conversation', 
            'message_body', 'sent_at'
        ]
        read_only_fields = ['id', 'sent_at', 'sender']
        extra_kwargs = {
            'conversation': {'required': True}
        }
    
    def validate_sender_id(self, value):
        """Validate that the sender_id corresponds to an existing user."""
        try:
            User.objects.get(id=value)
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
        sender = User.objects.get(id=sender_id)
        message = Message.objects.create(sender=sender, **validated_data)
        return message


class ConversationParticipantSerializer(serializers.ModelSerializer):
    """
    Serializer for conversation participants.
    
    Handles the many-to-many relationship between users and conversations.
    """
    user = UserSummarySerializer(read_only=True)
    user_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = ConversationParticipant
        fields = ['user', 'user_id', 'joined_at']
        read_only_fields = ['joined_at']
    
    def validate_user_id(self, value):
        """Validate that the user_id corresponds to an existing user."""
        try:
            User.objects.get(id=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("User with this ID does not exist.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model.
    
    Includes participants and messages with proper nested relationships.
    """
    participants = UserSummarySerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    participant_count = serializers.SerializerMethodField()
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = [
            'id', 'participants', 'participant_count',
            'messages', 'message_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def get_participant_count(self, obj):
        """Return the number of participants in the conversation."""
        return obj.participants.count()
    
    def get_message_count(self, obj):
        """Return the number of messages in the conversation."""
        return obj.messages.count()


class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new conversations.
    
    Handles participant assignment during conversation creation.
    """
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=True
    )
    
    class Meta:
        model = Conversation
        fields = ['id', 'participant_ids', 'created_at']
        read_only_fields = ['id', 'created_at']
    
    def validate_participant_ids(self, value):
        """Validate that all participant IDs correspond to existing users."""
        if len(value) < 2:
            raise serializers.ValidationError(
                "A conversation must have at least 2 participants."
            )
        
        # Check for duplicate participants
        if len(value) != len(set(value)):
            raise serializers.ValidationError(
                "Duplicate participants are not allowed."
            )
        
        # Verify all users exist
        existing_users = User.objects.filter(id__in=value)
        if len(existing_users) != len(value):
            raise serializers.ValidationError(
                "One or more user IDs do not correspond to existing users."
            )
        
        return value
    
    def create(self, validated_data):
        """Create a conversation and add participants."""
        participant_ids = validated_data.pop('participant_ids')
        conversation = Conversation.objects.create(**validated_data)
        
        # Add participants to the conversation
        for user_id in participant_ids:
            user = User.objects.get(id=user_id)
            ConversationParticipant.objects.create(
                conversation=conversation,
                user=user
            )
        
        return conversation


class ConversationDetailSerializer(ConversationSerializer):
    """
    Detailed conversation serializer with full message content.
    
    Used for retrieving complete conversation details including
    all messages with sender information.
    """
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta(ConversationSerializer.Meta):
        fields = [
            'id', 'participants', 'participant_count',
            'messages', 'message_count', 'created_at'
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
        fields = ['sender_id', 'conversation', 'message_body']
        extra_kwargs = {
            'conversation': {'required': True}
        }
    
    def validate_message_body(self, value):
        """Validate that message body is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value
    
    def validate(self, data):
        """Validate that the sender is a participant in the conversation."""
        sender_id = data.get('sender_id')
        conversation = data.get('conversation')
        
        # Check if sender is a participant in the conversation
        if not conversation.participants.filter(id=sender_id).exists():
            raise serializers.ValidationError(
                "Sender must be a participant in the conversation."
            )
        
        return data
    
    def create(self, validated_data):
        """Create a message with proper sender assignment."""
        sender_id = validated_data.pop('sender_id')
        sender = User.objects.get(id=sender_id)
        message = Message.objects.create(sender=sender, **validated_data)
        return message 