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

### Nested Endpoints
- `GET/POST /api/conversations/{id}/messages/` - Messages within a conversation
- `GET /api/conversations/{id}/messages/my_messages/` - User's messages in conversation
- `GET /api/conversations/{id}/messages/search/?q=query` - Search messages in conversation

### Custom Actions
- `POST /api/conversations/{id}/add_participant/` - Add participant
- `POST /api/conversations/{id}/remove_participant/` - Remove participant
- `GET /api/conversations/{id}/participants/` - List participants
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
- **Filter**: `?sender=uuid&conversation=uuid&sent_at=2024-01-01`
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

# NestedDefaultRouter for conversation messages
conversations_router = routers.NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversations_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversations_router.urls)),
    path('', include('rest_framework.urls')),
]
```

## Database Schema

### User Table

- `id` (UUID, Primary Key)
- `first_name` (VARCHAR, NOT NULL)
- `last_name` (VARCHAR, NOT NULL)
- `email` (VARCHAR, UNIQUE, NOT NULL)
- `phone_number` (VARCHAR, NULL)
- `role` (ENUM: 'guest', 'host', 'admin', NOT NULL)
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### Conversation Table

- `id` (UUID, Primary Key)
- `created_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

### Message Table

- `id` (UUID, Primary Key)
- `sender_id` (Foreign Key, references User)
- `conversation_id` (Foreign Key, references Conversation)
- `message_body` (TEXT, NOT NULL)
- `sent_at` (TIMESTAMP, DEFAULT CURRENT_TIMESTAMP)

## Features

- **Custom User Model**: Extends Django's AbstractUser with additional fields
- **UUID Primary Keys**: Enhanced security and scalability
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