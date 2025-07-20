#!/usr/bin/env python3
"""
Admin configuration for the chats app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, ConversationParticipant, Message


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for the custom User model."""
    model = User
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'created_at')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'created_at')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """Admin configuration for the Conversation model."""
    list_display = ('id', 'created_at', 'participant_count')
    list_filter = ('created_at',)
    search_fields = ('id',)
    readonly_fields = ('id', 'created_at')
    
    def participant_count(self, obj):
        """Return the number of participants in the conversation."""
        return obj.participants.count()
    participant_count.short_description = 'Participants'


@admin.register(ConversationParticipant)
class ConversationParticipantAdmin(admin.ModelAdmin):
    """Admin configuration for the ConversationParticipant model."""
    list_display = ('conversation', 'user', 'joined_at')
    list_filter = ('joined_at',)
    search_fields = ('conversation__id', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('joined_at',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin configuration for the Message model."""
    list_display = ('id', 'sender', 'conversation', 'message_body', 'sent_at')
    list_filter = ('sent_at', 'sender__role')
    search_fields = ('message_body', 'sender__email', 'sender__first_name', 'sender__last_name')
    readonly_fields = ('id', 'sent_at')
    raw_id_fields = ('sender', 'conversation')
