#!/usr/bin/env python3
"""
Integration test for all generator functionalities.
This script demonstrates how all the generators work together in a real-world scenario.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock data for testing (simulates database)
MOCK_USERS = [
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
    {'user_id': '04f8c1f5-0d6e-7f4f-1b2f-9e0b7d5f0a1b', 'name': 'John Smith', 'email': 'john.smith@example.com', 'age': 18},
    {'user_id': '05a9d2f6-1e7f-8f5f-2c3f-0f1c8e6f1b2c', 'name': 'Jane Doe', 'email': 'jane.doe@example.com', 'age': 15},
]


def demonstrate_streaming():
    """Demonstrate streaming individual users."""
    print("1. STREAMING INDIVIDUAL USERS")
    print("=" * 40)
    
    def stream_users():
        for user in MOCK_USERS:
            yield user
    
    count = 0
    for user in stream_users():
        count += 1
        print(f"User {count}: {user['name']} (Age: {user['age']})")
        if count >= 5:  # Show first 5 users
            print("... (continuing)")
            break
    
    print(f"Total users available: {len(MOCK_USERS)}")
    print()


def demonstrate_batch_processing():
    """Demonstrate batch processing with age filtering."""
    print("2. BATCH PROCESSING (Age > 25)")
    print("=" * 40)
    
    def stream_users_in_batches(batch_size):
        for i in range(0, len(MOCK_USERS), batch_size):
            yield MOCK_USERS[i:i + batch_size]
    
    def batch_processing(batch_size):
        batch_num = 0
        total_processed = 0
        
        # Loop 1: Iterate through batches
        for batch in stream_users_in_batches(batch_size):
            batch_num += 1
            print(f"Processing batch {batch_num} ({len(batch)} users):")
            
            # Loop 2: Process each user in the batch
            for user in batch:
                # Loop 3: Filter users over age 25
                if user['age'] > 25:
                    print(f"  ✓ {user['name']} (Age: {user['age']})")
                    total_processed += 1
                else:
                    print(f"  ✗ {user['name']} (Age: {user['age']}) - Under 25")
        
        print(f"Total users over 25: {total_processed}")
    
    batch_processing(4)
    print()


def demonstrate_lazy_pagination():
    """Demonstrate lazy pagination."""
    print("3. LAZY PAGINATION")
    print("=" * 40)
    
    def paginate_users(page_size, offset):
        return MOCK_USERS[offset:offset + page_size]
    
    def lazy_paginate(page_size):
        offset = 0
        
        # Single loop to fetch pages lazily
        while True:
            page = paginate_users(page_size, offset)
            if not page:
                break
            yield page
            offset += page_size
    
    for page_num, page in enumerate(lazy_paginate(3), 1):
        print(f"Page {page_num}: {len(page)} users")
        for user in page:
            print(f"  - {user['name']} (Age: {user['age']})")
        if page_num >= 3:  # Show first 3 pages
            print("... (more pages available)")
            break
    
    print()


def demonstrate_memory_efficient_aggregation():
    """Demonstrate memory-efficient aggregation."""
    print("4. MEMORY-EFFICIENT AGGREGATION")
    print("=" * 40)
    
    def stream_user_ages():
        for user in MOCK_USERS:
            yield user['age']
    
    def calculate_average_age():
        total_age = 0
        user_count = 0
        
        # Loop 1: Iterate through ages using the generator
        for age in stream_user_ages():
            # Loop 2: Accumulate total age and count
            total_age += age
            user_count += 1
        
        if user_count > 0:
            average_age = total_age / user_count
            print(f"Average age of users: {average_age:.2f}")
            return average_age
        else:
            print("No users found")
            return 0
    
    # Show individual ages being processed
    print("Processing ages one by one:")
    age_gen = stream_user_ages()
    for i, age in enumerate(age_gen):
        print(f"  Age {i+1}: {age}")
        if i >= 4:  # Show first 5 ages
            print("  ... (continuing)")
            break
    
    # Calculate average
    print("\nCalculating average:")
    calculate_average_age()
    print()


def demonstrate_generator_benefits():
    """Demonstrate the benefits of using generators."""
    print("5. GENERATOR BENEFITS DEMONSTRATION")
    print("=" * 40)
    
    print("✓ Memory Efficiency:")
    print("  - Generators process one item at a time")
    print("  - No need to load entire dataset into memory")
    print("  - Suitable for large datasets")
    
    print("\n✓ Lazy Evaluation:")
    print("  - Data is generated on-demand")
    print("  - Can stop processing early if needed")
    print("  - Efficient for conditional processing")
    
    print("\n✓ Composability:")
    print("  - Generators can be chained together")
    print("  - Easy to create processing pipelines")
    print("  - Reusable components")
    
    # Demonstrate early termination
    print("\n✓ Early Termination Example:")
    def stream_names():
        for user in MOCK_USERS:
            print(f"    Processing: {user['name']}")
            yield user['name']
    
    print("  Looking for first name starting with 'J':")
    for name in stream_names():
        if name.startswith('J'):
            print(f"    Found: {name}")
            break
    
    print("  Notice: Processing stopped early!")
    print()


def main():
    """Main demonstration function."""
    print("PYTHON GENERATORS - COMPREHENSIVE DEMONSTRATION")
    print("=" * 60)
    print("This demonstrates all generator patterns implemented in the project.")
    print("All examples use mock data to show functionality without database dependency.")
    print("=" * 60)
    print()
    
    demonstrate_streaming()
    demonstrate_batch_processing()
    demonstrate_lazy_pagination()
    demonstrate_memory_efficient_aggregation()
    demonstrate_generator_benefits()
    
    print("=" * 60)
    print("DEMONSTRATION COMPLETE!")
    print("Key Features Demonstrated:")
    print("• Individual user streaming")
    print("• Batch processing with filtering")
    print("• Lazy pagination")
    print("• Memory-efficient aggregation")
    print("• Generator benefits and characteristics")
    print("=" * 60)


if __name__ == "__main__":
    main()
