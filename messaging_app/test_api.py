#!/usr/bin/env python3
"""
Quick API test script for the messaging application.

This script tests the main API endpoints to ensure they are working correctly.
Run this script after starting the Django development server.
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000"
API_BASE = f"{BASE_URL}/api"

# Test data
TEST_USER_1 = {
    "email": "testuser1@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User1",
    "role": "guest"
}

TEST_USER_2 = {
    "email": "testuser2@example.com",
    "password": "testpass123",
    "first_name": "Test",
    "last_name": "User2",
    "role": "guest"
}

class APITester:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.user_id = None
        self.conversation_id = None
        self.message_id = None
        self.participant_user_id = None
        
    def print_test(self, test_name, success, message=""):
        """Print test result with formatting."""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"   {message}")
        print()
        
    def make_request(self, method, endpoint, data=None, headers=None, expected_status=200):
        """Make HTTP request and return response."""
        url = f"{API_BASE}{endpoint}"
        
        if headers is None:
            headers = {}
            
        if self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
            
        if data:
            headers['Content-Type'] = 'application/json'
            
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data)
            elif method.upper() == 'PUT':
                response = requests.put(url, headers=headers, json=data)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            return response
            
        except requests.exceptions.ConnectionError:
            print("❌ FAIL Connection Error - Is the Django server running?")
            print("   Run: python manage.py runserver 8000")
            sys.exit(1)
        except Exception as e:
            print(f"❌ FAIL Request Error: {e}")
            return None
            
    def test_server_connection(self):
        """Test if the server is running."""
        print("🔍 Testing server connection...")
        response = requests.get(f"{BASE_URL}/admin/")
        success = response.status_code in [200, 302]  # 302 for redirect to login
        self.print_test("Server Connection", success)
        return success
        
    def test_user_registration(self):
        """Test user registration."""
        print("🔍 Testing user registration...")
        
        # Register first user
        response = self.make_request('POST', '/auth/register/', TEST_USER_1, expected_status=201)
        if response and response.status_code == 201:
            data = response.json()
            self.access_token = data['tokens']['access']
            self.refresh_token = data['tokens']['refresh']
            self.user_id = data['user']['id']
            self.print_test("User 1 Registration", True, f"User ID: {self.user_id}")
        else:
            self.print_test("User 1 Registration", False, f"Status: {response.status_code if response else 'No response'}")
            return False
            
        # Register second user
        response = self.make_request('POST', '/auth/register/', TEST_USER_2, expected_status=201)
        if response and response.status_code == 201:
            data = response.json()
            self.participant_user_id = data['user']['id']
            self.print_test("User 2 Registration", True, f"User ID: {self.participant_user_id}")
        else:
            self.print_test("User 2 Registration", False, f"Status: {response.status_code if response else 'No response'}")
            return False
            
        return True
        
    def test_user_login(self):
        """Test user login."""
        print("🔍 Testing user login...")
        
        login_data = {
            "email": TEST_USER_1["email"],
            "password": TEST_USER_1["password"]
        }
        
        response = self.make_request('POST', '/auth/login/', login_data, expected_status=200)
        if response and response.status_code == 200:
            data = response.json()
            self.access_token = data['tokens']['access']
            self.refresh_token = data['tokens']['refresh']
            self.print_test("User Login", True, f"Access token received")
        else:
            self.print_test("User Login", False, f"Status: {response.status_code if response else 'No response'}")
            return False
            
        return True
        
    def test_get_profile(self):
        """Test getting user profile."""
        print("🔍 Testing get profile...")
        
        response = self.make_request('GET', '/auth/profile/', expected_status=200)
        if response and response.status_code == 200:
            data = response.json()
            self.print_test("Get Profile", True, f"Email: {data['user']['email']}")
        else:
            self.print_test("Get Profile", False, f"Status: {response.status_code if response else 'No response'}")
            return False
            
        return True
        
    def test_create_conversation(self):
        """Test creating a conversation."""
        print("🔍 Testing conversation creation...")
        
        conversation_data = {
            "participant_id": self.participant_user_id
        }
        
        response = self.make_request('POST', '/conversations/', conversation_data, expected_status=201)
        if response and response.status_code == 201:
            data = response.json()
            self.conversation_id = data['conversation_id']
            self.print_test("Create Conversation", True, f"Conversation ID: {self.conversation_id}")
        else:
            self.print_test("Create Conversation", False, f"Status: {response.status_code if response else 'No response'}")
            return False
            
        return True
        
    def test_get_conversations(self):
        """Test getting conversations list."""
        print("🔍 Testing get conversations...")
        
        response = self.make_request('GET', '/conversations/', expected_status=200)
        if response and response.status_code == 200:
            data = response.json()
            self.print_test("Get Conversations", True, f"Count: {data['count']}")
        else:
            self.print_test("Get Conversations", False, f"Status: {response.status_code if response else 'No response'}")
            return False
            
        return True
        
    def test_send_message(self):
        """Test sending a message."""
        print("🔍 Testing message sending...")
        
        message_data = {
            "message_body": f"Test message sent at {datetime.now().isoformat()}"
        }
        
        response = self.make_request('POST', f'/conversations/{self.conversation_id}/messages/', message_data, expected_status=201)
        if response and response.status_code == 201:
            data = response.json()
            self.message_id = data['message_id']
            self.print_test("Send Message", True, f"Message ID: {self.message_id}")
        else:
            self.print_test("Send Message", False, f"Status: {response.status_code if response else 'No response'}")
            return False
            
        return True
        
    def test_get_messages(self):
        """Test getting messages."""
        print("🔍 Testing get messages...")
        
        response = self.make_request('GET', '/messages/', expected_status=200)
        if response and response.status_code == 200:
            data = response.json()
            self.print_test("Get Messages", True, f"Count: {data['count']}, Page Size: {data['page_size']}")
        else:
            self.print_test("Get Messages", False, f"Status: {response.status_code if response else 'No response'}")
            return False
            
        return True
        
    def test_message_filtering(self):
        """Test message filtering."""
        print("🔍 Testing message filtering...")
        
        response = self.make_request('GET', '/messages/?sent_after=2025-01-01T00:00:00Z', expected_status=200)
        if response and response.status_code == 200:
            data = response.json()
            self.print_test("Message Filtering", True, f"Filtered count: {data['count']}")
        else:
            self.print_test("Message Filtering", False, f"Status: {response.status_code if response else 'No response'}")
            return False
            
        return True
        
    def test_unauthorized_access(self):
        """Test unauthorized access."""
        print("🔍 Testing unauthorized access...")
        
        # Test without token
        response = requests.get(f"{API_BASE}/conversations/")
        if response.status_code == 401:
            self.print_test("Unauthorized Access", True, "Properly blocked without token")
        else:
            self.print_test("Unauthorized Access", False, f"Expected 401, got {response.status_code}")
            return False
            
        return True
        
    def test_invalid_token(self):
        """Test invalid token access."""
        print("🔍 Testing invalid token...")
        
        headers = {'Authorization': 'Bearer invalid_token_here'}
        response = requests.get(f"{API_BASE}/messages/", headers=headers)
        if response.status_code == 401:
            self.print_test("Invalid Token", True, "Properly rejected invalid token")
        else:
            self.print_test("Invalid Token", False, f"Expected 401, got {response.status_code}")
            return False
            
        return True
        
    def run_all_tests(self):
        """Run all tests."""
        print("🚀 Starting API Tests for Messaging Application")
        print("=" * 60)
        
        tests = [
            self.test_server_connection,
            self.test_user_registration,
            self.test_user_login,
            self.test_get_profile,
            self.test_create_conversation,
            self.test_get_conversations,
            self.test_send_message,
            self.test_get_messages,
            self.test_message_filtering,
            self.test_unauthorized_access,
            self.test_invalid_token,
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            try:
                if test():
                    passed += 1
            except Exception as e:
                print(f"❌ FAIL {test.__name__} - Exception: {e}")
                print()
                
        print("=" * 60)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! The API is working correctly.")
        else:
            print("⚠️  Some tests failed. Check the output above for details.")
            
        return passed == total

def main():
    """Main function."""
    tester = APITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 