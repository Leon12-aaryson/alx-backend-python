#!/usr/bin/python3
"""
Database seeding script for ALX_prodev MySQL database.
This script creates the database, table, and populates it with sample data.
"""

import mysql.connector
from mysql.connector import Error
import csv
import os
import uuid


def connect_db():
    """
    Connects to the MySQL database server.
    
    Returns:
        mysql.connector.connection: Database connection object or None if failed
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'  # Change this to your MySQL root password
        )
        if connection.is_connected():
            print("Successfully connected to MySQL server")
            return connection
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
        print("Database ALX_prodev created successfully")
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    
    Returns:
        mysql.connector.connection: Database connection object or None if failed
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',  # Change this to your MySQL root password
            database='ALX_prodev'
        )
        if connection.is_connected():
            print("Successfully connected to ALX_prodev database")
            return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3,0) NOT NULL,
            INDEX idx_user_id (user_id)
        )
        """
        
        cursor.execute(create_table_query)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
        
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """
    Inserts data from CSV file into the database if it does not exist.
    
    Args:
        connection: MySQL connection object
        csv_file: Path to the CSV file containing user data
    """
    try:
        cursor = connection.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM user_data")
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"Data already exists in table user_data ({count} rows)")
            cursor.close()
            return
            
        # Read CSV file and insert data
        if not os.path.exists(csv_file):
            print(f"CSV file {csv_file} not found")
            cursor.close()
            return
            
        insert_query = """
        INSERT IGNORE INTO user_data (user_id, name, email, age)
        VALUES (%s, %s, %s, %s)
        """
        
        with open(csv_file, 'r', newline='', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            rows_inserted = 0
            
            for row in csv_reader:
                try:
                    # Validate UUID format
                    uuid.UUID(row['user_id'])
                    
                    data = (
                        row['user_id'],
                        row['name'],
                        row['email'],
                        int(row['age'])
                    )
                    
                    cursor.execute(insert_query, data)
                    rows_inserted += 1
                    
                except (ValueError, KeyError) as e:
                    print(f"Skipping invalid row: {row} - Error: {e}")
                    continue
        
        connection.commit()
        cursor.close()
        print(f"Successfully inserted {rows_inserted} rows into user_data table")
        
    except Error as e:
        print(f"Error inserting data: {e}")
        if connection.is_connected():
            connection.rollback()


def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    
    Yields:
        tuple: Each row from the user_data table
    """
    connection = None
    try:
        connection = connect_to_prodev()
        if not connection:
            return
            
        cursor = connection.cursor()
        cursor.execute("SELECT user_id, name, email, age FROM user_data")
        
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
    except Error as e:
        print(f"Error streaming users: {e}")
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    # Test the functions
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
        print("Connection successful")

        connection = connect_to_prodev()
        if connection:
            create_table(connection)
            insert_data(connection, 'user_data.csv')
            
            cursor = connection.cursor()
            cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev'")
            result = cursor.fetchone()
            if result:
                print("Database ALX_prodev is present")
                
            cursor.execute("SELECT * FROM user_data LIMIT 5")
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            connection.close()
