#!/usr/bin/env python3
"""
Example usage of the database streaming generator.
This demonstrates how to use the generator to process large datasets efficiently.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from seed import stream_users
from seed import connect_to_prodev


def process_user_data():
    """
    Example function showing how to process user data using the generator.
    This approach is memory-efficient as it processes one record at a time.
    """
    print("Processing user data using generator...")
    
    user_count = 0
    total_age = 0
    
    try:
        for user in stream_users():
            user_count += 1
            total_age += user[3]  # age is at index 3
            print(f"Processing user {user_count}: {user[1]} ({user[3]} years old)")
            
            # You can add any processing logic here
            # For example, data validation, transformation, etc.
            
    except Exception as e:
        print(f"Error processing user data: {e}")
        return
    
    if user_count > 0:
        average_age = total_age / user_count
        print(f"\nSummary:")
        print(f"Total users processed: {user_count}")
        print(f"Average age: {average_age:.2f} years")
    else:
        print("No users found to process")


def demonstrate_memory_efficiency():
    """
    Demonstrate the memory efficiency of using generators vs loading all data.
    """
    print("\n" + "="*50)
    print("MEMORY EFFICIENCY DEMONSTRATION")
    print("="*50)
    
    # Method 1: Using Generator (Memory Efficient)
    print("\n1. Using Generator (Memory Efficient):")
    print("   - Only one record in memory at a time")
    print("   - Can handle datasets of any size")
    
    user_count = 0
    for user in stream_users():
        user_count += 1
        if user_count <= 3:  # Show first 3 users
            print(f"   User {user_count}: {user[1]}")
        elif user_count == 4:
            print("   ... (processing continues)")
            
    print(f"   Total users processed: {user_count}")
    
    # Method 2: Loading all data (Not recommended for large datasets)
    print("\n2. Alternative - Loading all data at once:")
    print("   - All records loaded into memory")
    print("   - May cause memory issues with large datasets")
    
    try:
        connection = connect_to_prodev()
        if connection:
            cursor = connection.cursor()
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            all_users = cursor.fetchall()  # This loads ALL data into memory
            print(f"   Loaded {len(all_users)} users into memory")
            cursor.close()
            connection.close()
        else:
            print("   Could not connect to database")
    except Exception as e:
        print(f"   Error: {e}")


if __name__ == "__main__":
    print("Database Streaming Generator Example")
    print("="*40)
    
    # Process user data using the generator
    process_user_data()
    
    # Demonstrate memory efficiency
    demonstrate_memory_efficiency()
    
    print("\n" + "="*50)
    print("Generator streaming completed successfully!")
    print("="*50)
