#!/usr/bin/env python3
"""
Middleware for logging user requests and implementing access controls.

This module contains custom middleware components for the messaging application,
including request logging, time-based access restrictions, rate limiting,
and role-based permissions.
"""

import logging
import time
from datetime import datetime, time as dt_time
from django.http import HttpResponseForbidden
from collections import defaultdict


class RequestLoggingMiddleware:
    """
    Middleware to log user requests with timestamp, user, and path information.
    
    This middleware intercepts all incoming requests and logs them to a file
    for debugging and auditing purposes.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware with the get_response callable.
        
        Args:
            get_response: The callable that takes a request and returns a response
        """
        self.get_response = get_response
        
        # Configure logging
        self.logger = logging.getLogger('request_logger')
        self.logger.setLevel(logging.INFO)
        
        # Create file handler if it doesn't exist
        if not self.logger.handlers:
            file_handler = logging.FileHandler('requests.log')
            formatter = logging.Formatter('%(message)s')
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
    
    def __call__(self, request):
        """
        Process the request and log the required information.
        
        Args:
            request: The HTTP request object
            
        Returns:
            The HTTP response object
        """
        # Get user information
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        
        # Log the request information
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        self.logger.info(log_message)
        
        # Process the request and get the response
        response = self.get_response(request)
        
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to the messaging app during certain hours.
    
    This middleware denies access (403 Forbidden) if users try to access
    the chat outside of 9PM to 6AM (night hours).
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware with the get_response callable.
        
        Args:
            get_response: The callable that takes a request and returns a response
        """
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Check current time and restrict access during off-hours.
        
        Args:
            request: The HTTP request object
            
        Returns:
            The HTTP response object or 403 Forbidden
        """
        current_time = datetime.now().time()
        start_time = dt_time(21, 0)  # 9 PM
        end_time = dt_time(6, 0)     # 6 AM
        
        # Check if current time is outside allowed hours (9PM to 6AM)
        if current_time < end_time or current_time >= start_time:
            # Allow access during night hours (9PM to 6AM)
            response = self.get_response(request)
        else:
            # Deny access during day hours (6AM to 9PM)
            return HttpResponseForbidden("Access denied: Chat is only available from 9PM to 6AM")
        
        return response


class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of chat messages per IP address within a time window.
    
    This middleware implements rate limiting by tracking POST requests from each IP
    and limiting them to 5 messages per minute.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware with the get_response callable.
        
        Args:
            get_response: The callable that takes a request and returns a response
        """
        self.get_response = get_response
        self.ip_requests = defaultdict(list)  # Track requests per IP
        self.max_requests = 5  # Maximum requests per time window
        self.time_window = 60  # Time window in seconds (1 minute)
    
    def __call__(self, request):
        """
        Track POST requests and implement rate limiting per IP address.
        
        Args:
            request: The HTTP request object
            
        Returns:
            The HTTP response object or 403 Forbidden if rate limit exceeded
        """
        # Only track POST requests (messages)
        if request.method == 'POST':
            ip_address = self._get_client_ip(request)
            current_time = time.time()
            
            # Clean old requests outside the time window
            self.ip_requests[ip_address] = [
                req_time for req_time in self.ip_requests[ip_address]
                if current_time - req_time < self.time_window
            ]
            
            # Check if rate limit exceeded
            if len(self.ip_requests[ip_address]) >= self.max_requests:
                return HttpResponseForbidden(
                    f"Rate limit exceeded: Maximum {self.max_requests} messages per minute allowed"
                )
            
            # Add current request to tracking
            self.ip_requests[ip_address].append(current_time)
        
        # Process the request and get the response
        response = self.get_response(request)
        
        return response
    
    def _get_client_ip(self, request):
        """
        Get the client IP address from the request.
        
        Args:
            request: The HTTP request object
            
        Returns:
            str: The client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RolePermissionMiddleware:
    """
    Middleware to check user roles before allowing access to specific actions.
    
    This middleware enforces role-based access control by checking if the user
    has admin or moderator privileges for certain endpoints.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware with the get_response callable.
        
        Args:
            get_response: The callable that takes a request and returns a response
        """
        self.get_response = get_response
        # Define protected paths that require admin/moderator access
        self.protected_paths = [
            '/api/admin/',
            '/api/moderate/',
            '/api/users/delete/',
            '/api/conversations/delete/',
        ]
    
    def __call__(self, request):
        """
        Check user role and restrict access to protected endpoints.
        
        Args:
            request: The HTTP request object
            
        Returns:
            The HTTP response object or 403 Forbidden if access denied
        """
        # Check if the current path requires role verification
        if any(request.path.startswith(path) for path in self.protected_paths):
            # Check if user is authenticated and has admin privileges
            if not request.user.is_authenticated:
                return HttpResponseForbidden("Authentication required")
            
            # Check if user has admin or moderator role
            # Assuming the User model has a role field or is_staff/is_superuser
            if not (request.user.is_staff or request.user.is_superuser or 
                   hasattr(request.user, 'role') and request.user.role in ['admin', 'moderator']):
                return HttpResponseForbidden("Admin or moderator access required")
        
        # Process the request and get the response
        response = self.get_response(request)
        
        return response 