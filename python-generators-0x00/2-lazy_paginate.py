#!/usr/bin/python3
"""
Lazy loading Paginated Data
Objective: Simulate fetching paginated data from the users database using a generator to lazily load each page
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import seed


def paginate_users(page_size, offset):
    """
    Fetch users from database with pagination.
    
    Args:
        page_size (int): Number of users per page
        offset (int): Starting position for the query
        
    Returns:
        list: List of user dictionaries for the current page
    """
    connection = seed.connect_to_prodev()
    if not connection:
        return []
        
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    cursor.close()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    Generator that lazily loads pages of users from the database.
    
    Args:
        page_size (int): Number of users per page
        
    Yields:
        list: Page of user dictionaries
    """
    offset = 0
    
    # Single loop to fetch pages lazily
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size


# Alias for the expected function name in the test
lazy_pagination = lazy_paginate


if __name__ == "__main__":
    # Test the lazy pagination
    print("Testing lazy pagination with page size 100...")
    for page_num, page in enumerate(lazy_paginate(100), 1):
        print(f"Page {page_num}: {len(page)} users")
        for user in page[:3]:  # Show first 3 users of each page
            print(f"  {user}")
        if page_num >= 2:  # Limit output for testing
            break
