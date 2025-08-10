from django.contrib import admin
from django.utils.html import format_html
from .models import User, Message, Notification, MessageHistory, Conversation


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin interface for User model with custom display and filtering.
    """
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'created_at')
    list_filter = ('role', 'is_active', 'created_at')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('id', 'created_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('email', 'username', 'first_name', 'last_name', 'password')
        }),
        ('Contact Information', {
            'fields': ('phone_number',)
        }),
        ('Permissions', {
            'fields': ('role', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('System Information', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for Message model with custom display and filtering.
    """
    list_display = ('sender_email', 'receiver_email', 'content_preview', 'timestamp', 'edited', 'is_read')
    list_filter = ('edited', 'is_read', 'timestamp', 'sender', 'receiver')
    search_fields = ('content', 'sender__email', 'receiver__email')
    readonly_fields = ('id', 'message_id', 'timestamp', 'edited_at')
    ordering = ('-timestamp',)
    
    def sender_email(self, obj):
        return obj.sender.email
    sender_email.short_description = 'Sender'
    
    def receiver_email(self, obj):
        return obj.receiver.email
    receiver_email.short_description = 'Receiver'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    fieldsets = (
        ('Message Information', {
            'fields': ('sender', 'receiver', 'content')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at', 'edited', 'edited_at')
        }),
        ('System Information', {
            'fields': ('id', 'message_id', 'timestamp'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Admin interface for Notification model with custom display and filtering.
    """
    list_display = ('user_email', 'notification_type', 'title_preview', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at', 'user')
    search_fields = ('title', 'content', 'user__email')
    readonly_fields = ('id', 'created_at', 'read_at')
    ordering = ('-created_at',)
    
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'User'
    
    def title_preview(self, obj):
        return obj.title[:50] + '...' if len(obj.title) > 50 else obj.title
    title_preview.short_description = 'Title Preview'
    
    fieldsets = (
        ('Notification Information', {
            'fields': ('user', 'message', 'notification_type', 'title', 'content')
        }),
        ('Status', {
            'fields': ('is_read', 'read_at')
        }),
        ('System Information', {
            'fields': ('id', 'created_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for MessageHistory model with custom display and filtering.
    """
    list_display = ('message_id', 'edited_by_email', 'edited_at', 'old_content_preview')
    list_filter = ('edited_at', 'edited_by')
    search_fields = ('old_content', 'edit_reason', 'message__id')
    readonly_fields = ('id', 'edited_at')
    ordering = ('-edited_at',)
    
    def message_id(self, obj):
        return str(obj.message.id)[:8] + '...'
    message_id.short_description = 'Message ID'
    
    def edited_by_email(self, obj):
        return obj.edited_by.email
    edited_by_email.short_description = 'Edited By'
    
    def old_content_preview(self, obj):
        return obj.old_content[:50] + '...' if len(obj.old_content) > 50 else obj.old_content
    old_content_preview.short_description = 'Old Content Preview'
    
    fieldsets = (
        ('History Information', {
            'fields': ('message', 'old_content', 'edited_by', 'edit_reason')
        }),
        ('System Information', {
            'fields': ('id', 'edited_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    """
    Admin interface for Conversation model with custom display and filtering.
    """
    list_display = ('conversation_id', 'participants_list', 'message_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('participants__email', 'participants__first_name')
    readonly_fields = ('id', 'conversation_id', 'created_at', 'updated_at')
    ordering = ('-updated_at',)
    
    def participants_list(self, obj):
        participants = obj.participants.all()
        return ', '.join([p.get_full_name() or p.email for p in participants])
    participants_list.short_description = 'Participants'
    
    def message_count(self, obj):
        return obj.message_set.count()
    message_count.short_description = 'Messages'
    
    fieldsets = (
        ('Conversation Information', {
            'fields': ('participants', 'is_active')
        }),
        ('System Information', {
            'fields': ('id', 'conversation_id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
