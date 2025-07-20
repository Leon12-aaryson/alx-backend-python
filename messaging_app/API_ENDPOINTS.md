# API Endpoints Documentation

This document lists all available API endpoints for the messaging application.

## Base URL
All API endpoints are prefixed with `/api/`

## Authentication
All endpoints require authentication. Use session authentication or basic authentication.

## Endpoints

### Users
- `GET /api/users/` - List users (filtered by permissions)
- `POST /api/users/` - Create new user
- `GET /api/users/{id}/` - Get user details
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Conversations
- `GET /api/conversations/` - List user's conversations
- `POST /api/conversations/` - Create new conversation
- `GET /api/conversations/{id}/` - Get conversation details
- `PUT /api/conversations/{id}/` - Update conversation
- `DELETE /api/conversations/{id}/` - Delete conversation

#### Conversation Custom Actions
- `POST /api/conversations/{id}/add_participant/` - Add user to conversation
- `POST /api/conversations/{id}/remove_participant/` - Remove user from conversation
- `GET /api/conversations/{id}/participants/` - List conversation participants
- `GET /api/conversations/{id}/messages/` - Get conversation messages

### Messages
- `GET /api/messages/` - List user's messages
- `POST /api/messages/` - Create new message
- `GET /api/messages/{id}/` - Get message details
- `PUT /api/messages/{id}/` - Update message
- `DELETE /api/messages/{id}/` - Delete message

#### Message Custom Actions
- `POST /api/messages/send_message/` - Send message to conversation
- `GET /api/messages/my_messages/` - Get messages sent by current user
- `GET /api/messages/search/?q=query` - Search messages by content
- `GET /api/messages/{id}/conversation_messages/` - Get messages from specific conversation

## URL Names for Reverse Lookup

### Users
- `chats:user-list` - User list endpoint
- `chats:user-detail` - User detail endpoint

### Conversations
- `chats:conversation-list` - Conversation list endpoint
- `chats:conversation-detail` - Conversation detail endpoint
- `chats:conversation-add-participant` - Add participant action
- `chats:conversation-remove-participant` - Remove participant action
- `chats:conversation-participants` - List participants action
- `chats:conversation-messages` - List messages action

### Messages
- `chats:message-list` - Message list endpoint
- `chats:message-detail` - Message detail endpoint
- `chats:message-send-message` - Send message action
- `chats:message-my-messages` - My messages action
- `chats:message-search` - Search messages action
- `chats:message-conversation-messages` - Conversation messages action

### API Root
- `chats:api-root` - API root endpoint

## Example Usage

### Create a Conversation
```bash
POST /api/conversations/
Content-Type: application/json

{
    "participant_ids": ["user1-uuid", "user2-uuid"]
}
```

### Send a Message
```bash
POST /api/messages/send_message/
Content-Type: application/json

{
    "conversation": "conversation-uuid",
    "message_body": "Hello everyone!"
}
```

### Add Participant to Conversation
```bash
POST /api/conversations/{conversation-id}/add_participant/
Content-Type: application/json

{
    "user_id": "new-user-uuid"
}
```

### Search Messages
```bash
GET /api/messages/search/?q=hello
```

## Response Format
All endpoints return JSON responses with proper HTTP status codes.

### Success Response
```json
{
    "id": "uuid",
    "field1": "value1",
    "field2": "value2"
}
```

### Error Response
```json
{
    "error": "Error message description"
}
```

## Pagination
List endpoints support pagination with the following parameters:
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20)

### Paginated Response
```json
{
    "count": 100,
    "next": "http://example.com/api/endpoint/?page=2",
    "previous": null,
    "results": [...]
}
``` 