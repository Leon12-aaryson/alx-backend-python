#!/usr/bin/env python3
"""
Custom pagination classes for the messaging application.

This module defines custom pagination classes to provide
consistent pagination across the API endpoints.
"""

from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    """
    Custom pagination for Message endpoints.
    
    Provides pagination with 20 messages per page by default,
    with customizable page size up to 100 messages.
    """
    
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        """
        Return a paginated response with custom format.
        
        Args:
            data: The paginated data
            
        Returns:
            Response object with pagination metadata
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
            'page_size': self.get_page_size(self.request),
        })


class ConversationPagination(PageNumberPagination):
    """
    Custom pagination for Conversation endpoints.
    
    Provides pagination with 10 conversations per page by default,
    with customizable page size up to 50 conversations.
    """
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        """
        Return a paginated response with custom format.
        
        Args:
            data: The paginated data
            
        Returns:
            Response object with pagination metadata
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
            'page_size': self.get_page_size(self.request),
        })


class UserPagination(PageNumberPagination):
    """
    Custom pagination for User endpoints.
    
    Provides pagination with 25 users per page by default,
    with customizable page size up to 100 users.
    """
    
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        """
        Return a paginated response with custom format.
        
        Args:
            data: The paginated data
            
        Returns:
            Response object with pagination metadata
        """
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'page': self.page.number,
            'pages': self.page.paginator.num_pages,
            'page_size': self.get_page_size(self.request),
        })


class LimitOffsetMessagePagination(LimitOffsetPagination):
    """
    Alternative pagination using limit/offset for Message endpoints.
    
    Useful for cases where page-based pagination is not preferred.
    """
    
    default_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    max_limit = 100
    
    def get_paginated_response(self, data):
        """
        Return a paginated response with custom format.
        
        Args:
            data: The paginated data
            
        Returns:
            Response object with pagination metadata
        """
        return Response({
            'count': self.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'limit': self.limit,
            'offset': self.offset,
        }) 