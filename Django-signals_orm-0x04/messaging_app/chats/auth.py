#!/usr/bin/env python3
"""
Authentication views for the messaging application.

This module provides JWT-based authentication endpoints including
login, registration, and token refresh functionality.
"""

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User
from .serializers import UserSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom token obtain pair view that returns user information along with tokens.
    """
    
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Get user information
            user = User.objects.get(email=request.data['email'])
            user_data = UserSerializer(user).data
            
            # Add user data to response
            response.data['user'] = user_data
        
        return response


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Register a new user and return JWT tokens.
    
    Expected payload:
    {
        "email": "user@example.com",
        "password": "securepassword",
        "first_name": "John",
        "last_name": "Doe",
        "role": "guest"
    }
    """
    try:
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not request.data.get(field):
                return Response(
                    {'error': f'{field} is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Check if user already exists
        if User.objects.filter(email=request.data['email']).exists():
            return Response(
                {'error': 'User with this email already exists'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate password
        try:
            validate_password(request.data['password'])
        except ValidationError as e:
            return Response(
                {'error': 'Password validation failed', 'details': e.messages}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        user_data = {
            'email': request.data['email'],
            'password': request.data['password'],
            'first_name': request.data['first_name'],
            'last_name': request.data['last_name'],
            'role': request.data.get('role', 'guest'),
            'phone_number': request.data.get('phone_number', '')
        }
        
        user = User.objects.create_user(**user_data)
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Return user data and tokens
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': 'Registration failed', 'details': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    Authenticate user and return JWT tokens.
    
    Expected payload:
    {
        "email": "user@example.com",
        "password": "password"
    }
    """
    try:
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not password:
            return Response(
                {'error': 'Email and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authenticate user
        user = authenticate(request, email=email, password=password)
        
        if user is None:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        # Return user data and tokens
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': 'Login failed', 'details': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout(request):
    """
    Logout user by blacklisting the refresh token.
    
    Expected payload:
    {
        "refresh": "refresh_token_here"
    }
    """
    try:
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response(
                {'error': 'Refresh token is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response(
            {'message': 'Successfully logged out'}, 
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        return Response(
            {'error': 'Logout failed', 'details': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile(request):
    """
    Get current user's profile information.
    """
    try:
        user = request.user
        return Response({
            'user': UserSerializer(user).data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': 'Failed to get profile', 'details': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 