#!/usr/bin/env python3
"""
Test script to verify the generator implementation without database connection.
This demonstrates the generator pattern using mock data.
"""

def mock_stream_users():
    """
    Mock generator that simulates streaming users from a database.
    This is useful for testing the generator pattern without a database connection.
    """
    # Mock user data similar to what would come from the database
    users = [
        ('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67),
        ('006bfede-724d-4cdd-a2a6-59700f40d0da', 'Glenda Wisozk', 'Miriam21@gmail.com', 119),
        ('006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'Daniel Fahey IV', 'Delia.Lesch11@hotmail.com', 49),
        ('00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'Ronnie Bechtelar', 'Sandra19@yahoo.com', 22),
        ('00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'Alma Bechtelar', 'Shelly_Balistreri22@hotmail.com', 102),
    ]
    
    print("Starting to stream users...")
    for user in users:
        print(f"Yielding user: {user[1]}")
        yield user
    print("Finished streaming users.")


def test_generator():
    """Test the generator functionality."""
    print("Testing Generator Pattern")
    print("=" * 30)
    
    # Test the mock generator
    user_count = 0
    for user in mock_stream_users():
        user_count += 1
        print(f"Received user {user_count}: {user[1]} (Age: {user[3]})")
    
    print(f"\nTotal users processed: {user_count}")
    
    # Demonstrate generator characteristics
    print("\nGenerator Characteristics:")
    print("- Lazy evaluation: Data is produced on-demand")
    print("- Memory efficient: Only one item in memory at a time")
    print("- Iterable: Can be used in for loops")
    print("- One-time use: Once exhausted, you need to create a new generator")


if __name__ == "__main__":
    test_generator()
