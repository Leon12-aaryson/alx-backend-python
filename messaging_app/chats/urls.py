#!/usr/bin/env python3
"""
URL configuration for the chats app.

This module defines the URL patterns for the messaging application
including viewsets and custom actions.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ConversationViewSet, MessageViewSet

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

app_name = 'chats'

urlpatterns = [
    # Include the router URLs with proper API routing
    path('api/', include(router.urls)),
    
    # API root for browsable API
    path('api/', include('rest_framework.urls')),
] 