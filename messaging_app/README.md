# Messaging Application

A Django-based messaging application with REST API support.

## Project Overview

This project implements a messaging system with the following features:

- User management with role-based access (guest, host, admin)
- Conversation management between multiple users
- Message sending and retrieval within conversations
- RESTful API endpoints for all operations

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
│   ├── views.py           # API views
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
   pip install django djangorestframework
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
- **Database Indexing**: Optimized queries for performance
- **Admin Interface**: Full Django admin integration
- **REST API**: Ready for frontend integration

## Development

This project follows Django best practices:

- Modular app structure
- Custom user model
- Proper model relationships
- Database constraints and indexing
- Admin interface configuration
- REST framework integration 