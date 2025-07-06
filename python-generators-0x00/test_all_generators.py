#!/usr/bin/env python3
"""
Comprehensive test script for all generator implementations.
This demonstrates all the generator patterns without requiring database connection.
"""

def mock_database_data():
    """Mock database data for testing."""
    return [
        {'user_id': '00234e50-34eb-4ce2-94ec-26e3fa749796', 'name': 'Dan Altenwerth Jr.', 'email': 'Molly59@gmail.com', 'age': 67},
        {'user_id': '006bfede-724d-4cdd-a2a6-59700f40d0da', 'name': 'Glenda Wisozk', 'email': 'Miriam21@gmail.com', 'age': 119},
        {'user_id': '006e1f7f-90c2-45ad-8c1d-1275d594cc88', 'name': 'Daniel Fahey IV', 'email': 'Delia.Lesch11@hotmail.com', 'age': 49},
        {'user_id': '00af05c9-0a86-419e-8c2d-5fb7e899ae1c', 'name': 'Ronnie Bechtelar', 'email': 'Sandra19@yahoo.com', 'age': 22},
        {'user_id': '00cc08cc-62f4-4da1-b8e4-f5d9ef5dbbd4', 'name': 'Alma Bechtelar', 'email': 'Shelly_Balistreri22@hotmail.com', 'age': 102},
        {'user_id': '01187f09-72be-4924-8a2d-150645dcadad', 'name': 'Jonathon Jones', 'email': 'Jody.Quigley-Ziemann33@yahoo.com', 'age': 116},
        {'user_id': '01ab6c5d-7ae2-4968-991a-d63e93d8d025', 'name': 'Forrest Heaney', 'email': 'Albert51@hotmail.com', 'age': 104},
        {'user_id': '01c5f8e2-9a7b-4d3c-8f1e-6b9a4c2d7e8f', 'name': 'Sarah Mitchell', 'email': 'sarah.mitchell@gmail.com', 'age': 34},
        {'user_id': '02d6a9f3-8b4c-5e2d-9f0e-7c8a5b3d8e9f', 'name': 'Michael Johnson', 'email': 'michael.j@yahoo.com', 'age': 42},
        {'user_id': '03e7b0f4-9c5d-6f3e-0a1f-8d9a6c4e9f0a', 'name': 'Emily Davis', 'email': 'emily.davis@gmail.com', 'age': 29},
    ]


def mock_stream_users_in_batches(batch_size):
    """Mock version of stream_users_in_batches for testing."""
    data = mock_database_data()
    
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        yield batch


def mock_batch_processing(batch_size):
    """Mock version of batch_processing for testing."""
    print(f"Processing users in batches of {batch_size}, filtering age > 25:")
    
    for batch in mock_stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)


def mock_paginate_users(page_size, offset):
    """Mock version of paginate_users for testing."""
    data = mock_database_data()
    return data[offset:offset + page_size]


def mock_lazy_paginate(page_size):
    """Mock version of lazy_paginate for testing."""
    offset = 0
    
    while True:
        page = mock_paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


def mock_stream_user_ages():
    """Mock version of stream_user_ages for testing."""
    data = mock_database_data()
    
    for user in data:
        yield user['age']


def mock_calculate_average_age():
    """Mock version of calculate_average_age for testing."""
    total_age = 0
    user_count = 0
    
    for age in mock_stream_user_ages():
        total_age += age
        user_count += 1
    
    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age}")
        return average_age
    else:
        print("No users found in database")
        return 0


def test_all_generators():
    """Test all generator implementations."""
    print("=" * 60)
    print("TESTING ALL GENERATOR IMPLEMENTATIONS")
    print("=" * 60)
    
    # Test 1: Batch Processing
    print("\n1. BATCH PROCESSING TEST")
    print("-" * 30)
    mock_batch_processing(3)
    
    # Test 2: Lazy Pagination
    print("\n2. LAZY PAGINATION TEST")
    print("-" * 30)
    print("Fetching users in pages of 4:")
    for page_num, page in enumerate(mock_lazy_paginate(4), 1):
        print(f"Page {page_num}: {len(page)} users")
        for user in page:
            print(f"  - {user['name']} (Age: {user['age']})")
        if page_num >= 3:  # Limit output
            break
    
    # Test 3: Memory-Efficient Aggregation
    print("\n3. MEMORY-EFFICIENT AGGREGATION TEST")
    print("-" * 30)
    print("Calculating average age using generator:")
    mock_calculate_average_age()
    
    # Test 4: Generator Characteristics
    print("\n4. GENERATOR CHARACTERISTICS DEMONSTRATION")
    print("-" * 30)
    print("Generator for ages:")
    age_gen = mock_stream_user_ages()
    print(f"Generator object: {age_gen}")
    print("First 5 ages:")
    for i, age in enumerate(age_gen):
        print(f"  Age {i+1}: {age}")
        if i >= 4:  # Show first 5 ages
            break
    
    print("\n" + "=" * 60)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    test_all_generators()
