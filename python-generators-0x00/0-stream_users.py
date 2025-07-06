#!/usr/bin/python3
"""
Generator that streams rows from the user_data table one by one.
"""

import mysql.connector
from mysql.connector import Error


def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    
    Yields:
        dict: Each row from the user_data table as a dictionary
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',  # Change this to your MySQL root password
            database='ALX_prodev'
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # Stream rows one by one
            while True:
                row = cursor.fetchone()
                if row is None:
                    break
                yield row
                
    except Error as e:
        print(f"Error streaming users: {e}")
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def stream_users_in_batches(batch_size=1000):
    """
    Generator that streams rows from the user_data table in batches.
    
    Args:
        batch_size (int): Number of rows to fetch in each batch
        
    Yields:
        list: Batch of rows from the user_data table
    """
    connection = None
    cursor = None
    
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',  # Change this to your MySQL root password
            database='ALX_prodev'
        )
        
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT user_id, name, email, age FROM user_data")
            
            # Stream rows in batches
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
                
    except Error as e:
        print(f"Error streaming users in batches: {e}")
    finally:
        # Clean up resources
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


if __name__ == "__main__":
    # Test the generator
    print("Streaming users one by one:")
    for user in stream_users():
        print(user)
        
    print("\nStreaming users in batches:")
    for batch in stream_users_in_batches(2):
        print(f"Batch of {len(batch)} users:")
        for user in batch:
            print(f"  {user}")
