from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Message, Notification, Conversation, MessageHistory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role', 'created_at']
        read_only_fields = ['id', 'created_at']


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for Message model."""
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    parent_message = serializers.PrimaryKeyRelatedField(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = [
            'id', 'message_id', 'sender', 'receiver', 'content', 'timestamp', 
            'edited', 'edited_at', 'is_read', 'read_at', 'parent_message', 'replies'
        ]
        read_only_fields = ['id', 'message_id', 'timestamp', 'edited_at']
    
    def get_replies(self, obj):
        """Get replies to this message."""
        replies = obj.replies.all()
        return MessageSerializer(replies, many=True, context=self.context).data


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for Notification model."""
    user = UserSerializer(read_only=True)
    message = MessageSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'notification_type', 'title', 'content', 'is_read', 'created_at', 'read_at']
        read_only_fields = ['id', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for Conversation model."""
    participants = UserSerializer(many=True, read_only=True)
    message_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Conversation
        fields = ['id', 'conversation_id', 'participants', 'created_at', 'updated_at', 'is_active', 'message_count']
        read_only_fields = ['id', 'conversation_id', 'created_at', 'updated_at']
    
    def get_message_count(self, obj):
        """Get the number of messages in this conversation."""
        return obj.messages.count()


class MessageHistorySerializer(serializers.ModelSerializer):
    """Serializer for MessageHistory model."""
    message = MessageSerializer(read_only=True)
    edited_by = UserSerializer(read_only=True)
    
    class Meta:
        model = MessageHistory
        fields = ['id', 'message', 'old_content', 'edited_by', 'edited_at', 'edit_reason']
        read_only_fields = ['id', 'edited_at']


class ThreadedMessageSerializer(serializers.ModelSerializer):
    """Serializer for threaded messages with replies."""
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    replies = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Message
        fields = [
            'id', 'message_id', 'sender', 'receiver', 'content', 'timestamp',
            'edited', 'edited_at', 'is_read', 'read_at', 'replies'
        ]
        read_only_fields = ['id', 'message_id', 'timestamp', 'edited_at'] 