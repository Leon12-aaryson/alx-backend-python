#!/usr/bin/python3
"""
Batch processing Large Data
Objective: Create a generator to fetch and process data in batches from the users database
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import mysql.connector
from mysql.connector import Error
import seed


def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows in batches from the users database.
    
    Args:
        batch_size (int): Number of users to fetch in each batch
        
    Yields:
        list: Batch of user dictionaries
    """
    connection = None
    cursor = None
    
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            return
            
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        # Fetch rows in batches
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
                
    except Error as e:
        print(f"Error streaming users in batches: {e}", file=sys.stderr)
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def batch_processing(batch_size):
    """
    Process each batch to filter users over the age of 25.
    
    Args:
        batch_size (int): Size of each batch to process
    """
    # Loop 1: Iterate through batches
    for batch in stream_users_in_batches(batch_size):
        # Loop 2: Process each user in the batch
        for user in batch:
            # Loop 3: Filter users over age 25
            if user['age'] > 25:
                print(user)


if __name__ == "__main__":
    # Test the functions
    print("Testing batch processing with batch size 50...")
    batch_processing(50)
