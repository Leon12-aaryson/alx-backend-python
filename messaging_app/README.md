# Messaging Application

A Django-based messaging application with REST API support.

## Project Overview

This project implements a messaging system with the following features:

- User management with role-based access (guest, host, admin)
- Conversation management between multiple users
- Message sending and retrieval within conversations
- RESTful API endpoints for all operations
- Nested routing for conversation messages
- Advanced filtering, searching, and ordering capabilities

## Project Structure

```text
messaging_app/
├── messaging_app/          # Main project settings
│   ├── __init__.py
│   ├── settings.py         # Django settings
│   ├── urls.py            # Main URL configuration
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── chats/                 # Messaging app
│   ├── __init__.py
│   ├── admin.py           # Admin interface configuration
│   ├── models.py          # Data models
│   ├── views.py           # API views with filtering
│   ├── serializers.py     # DRF serializers
│   └── urls.py            # App URL configuration
├── manage.py              # Django management script
└── README.md              # This file
```

## Data Models

### User Model

- Extends Django's AbstractUser
- Uses UUID as primary key
- Email-based authentication
- Role-based access control (guest, host, admin)
- Phone number validation

### Conversation Model

- Tracks conversations between multiple users
- Many-to-many relationship with users through ConversationParticipant
- UUID primary key for security

### Message Model

- Contains message content and metadata
- Links to sender (User) and conversation
- Timestamped for chronological ordering
- Indexed for performance

## Setup Instructions

1. **Install Dependencies**

   ```bash
   pip install django djangorestframework drf-nested-routers django-filter
   ```

2. **Run Migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser**

   ```bash
   python manage.py createsuperuser
   ```

4. **Run Development Server**

   ```bash
   python manage.py runserver
   ```

## API Endpoints

The application provides RESTful API endpoints for:

- User management (CRUD operations)
- Conversation management
- Message sending and retrieval
- Authentication and authorization
- Advanced filtering and searching

### Core Endpoints
- `GET/POST /api/users/` - User management
- `GET/POST /api/conversations/` - Conversation management
- `GET/POST /api/messages/` - Message management

### Conversation Endpoints
- `GET /api/conversations/` - List all conversations for the authenticated user
- `POST /api/conversations/` - Create a new conversation
- `GET /api/conversations/{id}/` - Get conversation details
- `PUT/PATCH /api/conversations/{id}/` - Update conversation
- `DELETE /api/conversations/{id}/` - Delete conversation
- `GET /api/conversations/{id}/participant/` - Get conversation participant

### Message Endpoints
- `GET /api/messages/` - List all messages sent by the authenticated user
- `POST /api/messages/` - Create a new message
- `GET /api/messages/{id}/` - Get message details
- `PUT/PATCH /api/messages/{id}/` - Update message (only by sender)
- `DELETE /api/messages/{id}/` - Delete message (only by sender)
- `POST /api/messages/send_message/` - Send a message
- `GET /api/messages/my_messages/` - Get user's messages
- `GET /api/messages/search/?q=query` - Search messages by content

### Custom Actions
- `GET /api/conversations/{id}/participant/` - Get conversation participant
- `POST /api/messages/send_message/` - Send message
- `GET /api/messages/my_messages/` - User's messages
- `GET /api/messages/search/?q=query` - Search messages

### Authentication Endpoints
- `/api-auth/login/` - REST framework login
- `/api-auth/logout/` - REST framework logout

### Filtering and Search
All list endpoints support filtering, searching, and ordering:

#### Users
- **Filter**: `?role=guest&is_active=true`
- **Search**: `?search=john`
- **Order**: `?ordering=-created_at,email`

#### Conversations
- **Filter**: `?created_at=2024-01-01`
- **Search**: `?search=john@example.com`
- **Order**: `?ordering=-created_at`

#### Messages
- **Filter**: `?sender_id=uuid&sent_at=2024-01-01`
- **Search**: `?search=hello`
- **Order**: `?ordering=-sent_at`

## URL Configuration

### Main Project URLs (`messaging_app/urls.py`)
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chats.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
```

### App URLs (`chats/urls.py`)
```python
# DefaultRouter for main endpoints
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_framework.urls')),
]
```

## Database Schema

### User Table
- `id` (UUID, Primary Key)
- `user_id` (UUID, Unique, NOT NULL)
- `password` (VARCHAR(128), NOT NULL)
- `first_name` (VARCHAR, NOT NULL)
- `last_name` (VARCHAR, NOT NULL)
- `email` (VARCHAR, UNIQUE, NOT NULL)
- `phone_number` (VARCHAR, NULL)
- `role` (ENUM: 'guest', 'host', 'admin', NOT NULL)
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### Conversation Table
- `id` (UUID, Primary Key)
- `conversation_id` (UUID, Unique, NOT NULL)
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### Message Table
- `id` (UUID, Primary Key)
- `message_id` (UUID, Unique, NOT NULL)
- `sender_id` (Foreign Key, references User)
- `conversation_id` (Foreign Key, references Conversation)
- `message_body` (TEXT, NOT NULL)
- `sent_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

## Features

- **Custom User Model**: Extends Django's AbstractUser with additional fields
- **UUID Primary Keys**: Enhanced security and scalability
- **Additional ID Fields**: Separate user_id, conversation_id, and message_id fields for better identification
- **Password Management**: Explicit password field with proper hashing
- **Role-Based Access**: Different user roles with appropriate permissions
- **Many-to-Many Relationships**: Flexible conversation participation
- **Nested Routing**: Messages within conversations using NestedDefaultRouter
- **Advanced Filtering**: Django-filter integration for complex queries
- **Search Functionality**: Full-text search across multiple fields
- **Ordering**: Flexible sorting by any field
- **Database Indexing**: Optimized queries for performance
- **Admin Interface**: Full Django admin integration
- **REST API**: Ready for frontend integration
- **Authentication**: Session and Basic authentication support

## Development

This project follows Django best practices:

- Modular app structure
- Custom user model
- Proper model relationships
- Database constraints and indexing
- Admin interface configuration
- REST framework integration
- Nested routing for complex relationships
- Advanced filtering and search capabilities

## Implementation Summary

### Viewsets Implementation

The application uses Django REST Framework viewsets to implement the API endpoints:

#### **ConversationViewSet** (`chats/views.py`)
```python
class ConversationViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    def get_queryset(self):
        """Return conversations where the current user is a participant."""
        user = self.request.user
        return Conversation.objects.filter(participants_id=user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return ConversationCreateSerializer
        return ConversationSerializer
    
    def perform_create(self, serializer):
        """Create conversation with current user as participant."""
        return serializer.save()
    
    @action(detail=True, methods=['get'])
    def participant(self, request, pk=None):
        """Get participant information in a conversation."""
        conversation = self.get_object()
        participant = conversation.participants_id
        serializer = UserSerializer(participant)
        return Response(serializer.data)
```

#### **MessageViewSet** (`chats/views.py`)
```python
class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    def get_queryset(self):
        """Return messages sent by the current user."""
        user = self.request.user
        return Message.objects.filter(sender_id=user)
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action in ['create', 'send_message']:
            return MessageCreateSerializer
        return MessageSerializer
    
    def perform_create(self, serializer):
        """Create message with current user as sender."""
        serializer.save(sender_id=self.request.user)
    
    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """Send a message."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save(sender_id=request.user)
            response_serializer = MessageSerializer(message)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### URL Configuration

The endpoints are configured using `routers.DefaultRouter()`:

```python
# chats/urls.py
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('rest_framework.urls')),
]
```

### Endpoint Functionality

#### **Creating Conversations**
- **Endpoint**: `POST /api/conversations/`
- **Method**: `ConversationViewSet.create()`
- **Serializer**: `ConversationCreateSerializer`
- **Functionality**: Creates a new conversation with the current user as participant

#### **Sending Messages**
- **Endpoint**: `POST /api/messages/send_message/`
- **Method**: `MessageViewSet.send_message()`
- **Serializer**: `MessageCreateSerializer`
- **Functionality**: Sends a message with the current user as sender

#### **Listing Conversations**
- **Endpoint**: `GET /api/conversations/`
- **Method**: `ConversationViewSet.list()`
- **Serializer**: `ConversationSerializer`
- **Functionality**: Lists all conversations where the user is a participant

#### **Listing Messages**
- **Endpoint**: `GET /api/messages/`
- **Method**: `MessageViewSet.list()`
- **Serializer**: `MessageSerializer`
- **Functionality**: Lists all messages sent by the current user 