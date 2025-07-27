#!/usr/bin/env python3
"""
Admin configuration for the chats app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Conversation, Message


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Admin configuration for the custom User model."""
    model = User
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'created_at')
    fieldsets = (
        (None, {'fields': ('email', 'password_hash')}),
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
    list_display = ('conversation_id', 'participants_id', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('conversation_id', 'participants_id__email', 'participants_id__first_name')
    readonly_fields = ('conversation_id', 'created_at')
    raw_id_fields = ('participants_id',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin configuration for the Message model."""
    list_display = ('message_id', 'sender_id', 'message_body', 'sent_at')
    list_filter = ('sent_at', 'sender_id__role')
    search_fields = ('message_body', 'sender_id__email', 'sender_id__first_name', 'sender_id__last_name')
    readonly_fields = ('message_id', 'sent_at')
    raw_id_fields = ('sender_id',)
