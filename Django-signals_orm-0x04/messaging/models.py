from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from datetime import datetime
from .managers import UnreadMessagesManager


class CustomUserManager(BaseUserManager):
    """
    Custom user manager for email-based authentication.
    """
    
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser.
    Uses UUID as primary key and email as username field.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, choices=[
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
        ('moderator', 'Moderator')
    ], default='guest')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.get_full_name()})"

    class Meta:
        db_table = 'messaging_user'





class Message(models.Model):
    """
    Message model for storing chat messages between users.
    Includes fields for tracking edits and message history.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    # New field for threaded conversations
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')

    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"Message from {self.sender.email} to {self.receiver.email} at {self.timestamp}"

    class Meta:
        db_table = 'messaging_message'
        ordering = ['-timestamp']


class Notification(models.Model):
    """
    Notification model for storing user notifications.
    Automatically created when new messages are received.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=[
        ('new_message', 'New Message'),
        ('message_edited', 'Message Edited'),
        ('message_deleted', 'Message Deleted'),
    ], default='new_message')
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Notification for {self.user.email}: {self.title}"

    class Meta:
        db_table = 'messaging_notification'
        ordering = ['-created_at']


class MessageHistory(models.Model):
    """
    MessageHistory model for tracking message edits.
    Stores previous versions of messages before they are edited.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='message_edits')
    edited_at = models.DateTimeField(auto_now_add=True)
    edit_reason = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"History for message {self.message.id} edited at {self.edited_at}"

    class Meta:
        db_table = 'messaging_messagehistory'
        ordering = ['-edited_at']
        verbose_name_plural = 'Message Histories'


class Conversation(models.Model):
    """
    Conversation model for grouping messages between users.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        participant_names = [user.get_full_name() or user.email for user in self.participants.all()]
        return f"Conversation between {', '.join(participant_names)}"

    class Meta:
        db_table = 'messaging_conversation'
        ordering = ['-updated_at']
