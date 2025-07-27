# Messaging App API Testing

This directory contains the complete API testing setup for the Django messaging application.

## 📁 Files

- **`post_man-Collections`**: Complete Postman collection with all API endpoints
- **`test_api.py`**: Automated Python test script for quick API validation
- **`README.md`**: This file with testing instructions

## 🚀 Quick Start

### Option 1: Postman Testing (Recommended)

1. **Import Collection**:
   - Open Postman
   - Click "Import" button
   - Select the `post_man-Collections` file
   - The collection will be imported with all endpoints organized

2. **Set Up Environment**:
   - Create a new environment in Postman
   - Add these variables:
     - `base_url`: `http://127.0.0.1:8000`
     - `access_token`: (leave empty, will be filled after login)
     - `refresh_token`: (leave empty, will be filled after login)
     - `user_id`: (leave empty, will be filled after login)
     - `conversation_id`: (leave empty, will be filled after creating conversation)
     - `message_id`: (leave empty, will be filled after creating message)
     - `participant_user_id`: (leave empty, will be filled after creating second user)

3. **Start Testing**:
   - Start the Django server: `python manage.py runserver 8000`
   - Follow the collection folders in order:
     1. **Authentication** - Register and login users
     2. **Users** - Test user management
     3. **Conversations** - Test conversation creation and management
     4. **Messages** - Test message sending and retrieval
     5. **Testing Scenarios** - Test security and edge cases

### Option 2: Automated Testing

1. **Start Server**:
   ```bash
   python manage.py runserver 8000
   ```

2. **Run Tests**:
   ```bash
   python test_api.py
   ```

3. **Review Results**:
   - Check the test output for any failures
   - All tests should pass for a fully working API

## 🧪 Testing Scenarios

### Authentication Flow
1. Register a new user → Get JWT tokens
2. Login with credentials → Get fresh tokens
3. Use access token for API calls
4. Refresh token when expired
5. Logout to blacklist refresh token

### Conversation Testing
1. Create conversation between two users
2. List user's conversations
3. Get conversation details
4. Send messages to conversation
5. Retrieve conversation messages

### Message Testing
1. Send standalone messages
2. Send messages to conversations
3. List user's messages with pagination
4. Filter messages by time and content
5. Search messages by content
6. Update and delete messages

### Security Testing
1. Test unauthorized access (should return 401)
2. Test invalid tokens (should return 401)
3. Test access to other user's data (should return 403)
4. Verify user isolation and permissions

## 📊 Expected Results

### Successful Responses
- **Registration/Login**: 201/200 with user data and JWT tokens
- **Protected Endpoints**: 200 with requested data
- **Pagination**: JSON with count, next, previous, and results
- **Filtering**: Filtered results based on query parameters

### Error Responses
- **401 Unauthorized**: Missing or invalid authentication
- **403 Forbidden**: Insufficient permissions
- **400 Bad Request**: Invalid request data
- **404 Not Found**: Resource doesn't exist

## 🔧 Troubleshooting

### Common Issues

1. **"Connection refused"**
   - Ensure Django server is running on port 8000
   - Check if the server started without errors

2. **"401 Unauthorized"**
   - Verify access token is valid and not expired
   - Check Authorization header format: `Bearer <token>`
   - Refresh token or login again if needed

3. **"403 Forbidden"**
   - Check user permissions and role
   - Ensure user has appropriate access rights
   - Verify user is trying to access their own data

4. **"400 Bad Request"**
   - Check request body format and required fields
   - Verify JSON syntax is correct
   - Ensure all required parameters are provided

### Environment Setup

If you encounter Python environment issues:
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

## 📝 Testing Checklist

- [ ] User registration works
- [ ] User login works
- [ ] JWT tokens are generated correctly
- [ ] Protected endpoints require authentication
- [ ] Users can only access their own conversations
- [ ] Users can only modify their own messages
- [ ] Pagination works correctly
- [ ] Filtering works correctly
- [ ] Search functionality works
- [ ] Unauthorized access is properly blocked
- [ ] Invalid tokens are rejected
- [ ] Token refresh works
- [ ] Logout works

## 🎯 Advanced Testing

### Load Testing
- Create multiple users
- Send many messages
- Test pagination with large datasets
- Test concurrent access

### Edge Cases
- Test with very long message content
- Test with special characters in messages
- Test with empty or null values
- Test with malformed JSON

### Security Testing
- Test SQL injection attempts
- Test XSS attempts
- Test CSRF protection
- Test rate limiting (if implemented)

## 📞 Support

If you encounter issues:
1. Check the Django server logs for errors
2. Verify all dependencies are installed
3. Ensure the database is properly migrated
4. Check that all required environment variables are set

The API testing setup is designed to thoroughly validate all aspects of the messaging application's functionality, security, and performance. 