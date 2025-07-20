#!/usr/bin/env python3
"""
URL configuration for the chats app.

This module defines the URL patterns for the messaging application
including viewsets and custom actions with nested routing.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

# Create nested routers for conversations and their messages
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

app_name = 'chats'

urlpatterns = [
    # Include the router URLs
    path('', include(router.urls)),
    
    # Include nested router URLs
    path('', include(conversations_router.urls)),
    
    # API root for browsable API
    path('', include('rest_framework.urls')),
] 