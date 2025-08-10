#!/usr/bin/env python3
"""
Custom filters for the messaging application.

This module defines custom filters for messages and conversations
to enable filtering by various criteria including time ranges and participants.
"""

import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from datetime import datetime, timedelta
from .models import Message, Conversation, User


class MessageFilter(filters.FilterSet):
    """
    Custom filter for Message model.
    
    Provides filtering capabilities for:
    - Messages within a time range
    - Messages from specific users
    - Messages in specific conversations
    - Message content search
    """
    
    # Time range filters
    sent_after = filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='gte',
        help_text='Filter messages sent after this datetime (ISO format)'
    )
    sent_before = filters.DateTimeFilter(
        field_name='sent_at',
        lookup_expr='lte',
        help_text='Filter messages sent before this datetime (ISO format)'
    )
    
    # Date range filters (for easier date-based filtering)
    sent_date = filters.DateFilter(
        field_name='sent_at',
        lookup_expr='date',
        help_text='Filter messages sent on a specific date (YYYY-MM-DD)'
    )
    sent_date_after = filters.DateFilter(
        field_name='sent_at',
        lookup_expr='date__gte',
        help_text='Filter messages sent after this date (YYYY-MM-DD)'
    )
    sent_date_before = filters.DateFilter(
        field_name='sent_at',
        lookup_expr='date__lte',
        help_text='Filter messages sent before this date (YYYY-MM-DD)'
    )
    
    # User filters
    sender_email = filters.CharFilter(
        field_name='sender_id__email',
        lookup_expr='icontains',
        help_text='Filter messages by sender email (partial match)'
    )
    sender_name = filters.CharFilter(
        method='filter_by_sender_name',
        help_text='Filter messages by sender name (first or last name)'
    )
    
    # Conversation filters
    conversation_id = filters.UUIDFilter(
        field_name='conversation__conversation_id',
        help_text='Filter messages by conversation ID'
    )
    
    # Content filters
    message_content = filters.CharFilter(
        field_name='message_body',
        lookup_expr='icontains',
        help_text='Filter messages by content (partial match)'
    )
    
    # Time-based filters
    last_hour = filters.BooleanFilter(
        method='filter_last_hour',
        help_text='Filter messages sent in the last hour'
    )
    last_24_hours = filters.BooleanFilter(
        method='filter_last_24_hours',
        help_text='Filter messages sent in the last 24 hours'
    )
    last_7_days = filters.BooleanFilter(
        method='filter_last_7_days',
        help_text='Filter messages sent in the last 7 days'
    )
    
    class Meta:
        model = Message
        fields = {
            'sender_id': ['exact'],
            'conversation': ['exact'],
            'sent_at': ['exact', 'gte', 'lte'],
            'message_body': ['exact', 'icontains'],
        }
    
    def filter_by_sender_name(self, queryset, name, value):
        """
        Filter messages by sender's first or last name.
        
        Args:
            queryset: The message queryset
            name: The filter field name
            value: The search value
            
        Returns:
            Filtered queryset
        """
        return queryset.filter(
            Q(sender_id__first_name__icontains=value) |
            Q(sender_id__last_name__icontains=value)
        )
    
    def filter_last_hour(self, queryset, name, value):
        """
        Filter messages sent in the last hour.
        
        Args:
            queryset: The message queryset
            name: The filter field name
            value: Boolean value indicating whether to apply filter
            
        Returns:
            Filtered queryset
        """
        if value:
            one_hour_ago = datetime.now() - timedelta(hours=1)
            return queryset.filter(sent_at__gte=one_hour_ago)
        return queryset
    
    def filter_last_24_hours(self, queryset, name, value):
        """
        Filter messages sent in the last 24 hours.
        
        Args:
            queryset: The message queryset
            name: The filter field name
            value: Boolean value indicating whether to apply filter
            
        Returns:
            Filtered queryset
        """
        if value:
            one_day_ago = datetime.now() - timedelta(days=1)
            return queryset.filter(sent_at__gte=one_day_ago)
        return queryset
    
    def filter_last_7_days(self, queryset, name, value):
        """
        Filter messages sent in the last 7 days.
        
        Args:
            queryset: The message queryset
            name: The filter field name
            value: Boolean value indicating whether to apply filter
            
        Returns:
            Filtered queryset
        """
        if value:
            seven_days_ago = datetime.now() - timedelta(days=7)
            return queryset.filter(sent_at__gte=seven_days_ago)
        return queryset


class ConversationFilter(filters.FilterSet):
    """
    Custom filter for Conversation model.
    
    Provides filtering capabilities for:
    - Conversations by participant
    - Conversations within a time range
    - Conversations with specific users
    """
    
    # Participant filters
    participant_email = filters.CharFilter(
        field_name='participants_id__email',
        lookup_expr='icontains',
        help_text='Filter conversations by participant email'
    )
    participant_name = filters.CharFilter(
        method='filter_by_participant_name',
        help_text='Filter conversations by participant name'
    )
    
    # Time filters
    created_after = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='gte',
        help_text='Filter conversations created after this datetime'
    )
    created_before = filters.DateTimeFilter(
        field_name='created_at',
        lookup_expr='lte',
        help_text='Filter conversations created before this datetime'
    )
    
    # Message count filters
    has_messages = filters.BooleanFilter(
        method='filter_has_messages',
        help_text='Filter conversations that have messages'
    )
    message_count_min = filters.NumberFilter(
        method='filter_message_count_min',
        help_text='Filter conversations with at least this many messages'
    )
    message_count_max = filters.NumberFilter(
        method='filter_message_count_max',
        help_text='Filter conversations with at most this many messages'
    )
    
    class Meta:
        model = Conversation
        fields = {
            'participants_id': ['exact'],
            'created_at': ['exact', 'gte', 'lte'],
        }
    
    def filter_by_participant_name(self, queryset, name, value):
        """
        Filter conversations by participant's first or last name.
        
        Args:
            queryset: The conversation queryset
            name: The filter field name
            value: The search value
            
        Returns:
            Filtered queryset
        """
        return queryset.filter(
            Q(participants_id__first_name__icontains=value) |
            Q(participants_id__last_name__icontains=value)
        )
    
    def filter_has_messages(self, queryset, name, value):
        """
        Filter conversations that have messages.
        
        Args:
            queryset: The conversation queryset
            name: The filter field name
            value: Boolean value indicating whether to apply filter
            
        Returns:
            Filtered queryset
        """
        if value:
            return queryset.filter(messages__isnull=False).distinct()
        return queryset.filter(messages__isnull=True)
    
    def filter_message_count_min(self, queryset, name, value):
        """
        Filter conversations with at least a minimum number of messages.
        
        Args:
            queryset: The conversation queryset
            name: The filter field name
            value: Minimum message count
            
        Returns:
            Filtered queryset
        """
        return queryset.annotate(
            message_count=django_filters.Count('messages')
        ).filter(message_count__gte=value)
    
    def filter_message_count_max(self, queryset, name, value):
        """
        Filter conversations with at most a maximum number of messages.
        
        Args:
            queryset: The conversation queryset
            name: The filter field name
            value: Maximum message count
            
        Returns:
            Filtered queryset
        """
        return queryset.annotate(
            message_count=django_filters.Count('messages')
        ).filter(message_count__lte=value) 