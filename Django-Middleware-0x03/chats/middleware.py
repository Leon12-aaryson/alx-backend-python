#!/usr/bin/env python3
"""
Middleware for logging user requests.

This module contains custom middleware components for the messaging application,
including request logging functionality.
"""

import logging
from datetime import datetime


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