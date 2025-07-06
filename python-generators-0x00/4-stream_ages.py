#!/usr/bin/python3
"""
Memory-Efficient Aggregation with Generators
Objective: Use a generator to compute a memory-efficient aggregate function (average age) for a large dataset
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mysql.connector
from mysql.connector import Error
import seed


def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    
    Yields:
        int: User age
    """
    connection = None
    cursor = None
    
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            return
            
        cursor = connection.cursor()
        cursor.execute("SELECT age FROM user_data")
        
        # Stream ages one by one
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]  # age is the first (and only) column
                
    except Error as e:
        print(f"Error streaming user ages: {e}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def calculate_average_age():
    """
    Calculate the average age of all users using the generator.
    This is memory-efficient as it processes one age at a time.
    
    Returns:
        float: Average age of users
    """
    total_age = 0
    user_count = 0
    
    # Loop 1: Iterate through ages using the generator
    for age in stream_user_ages():
        # Loop 2: Accumulate total age and count
        total_age += age
        user_count += 1
    
    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age}")
        return average_age
    else:
        print("No users found in database")
        return 0


if __name__ == "__main__":
    # Calculate and display average age
    calculate_average_age()
