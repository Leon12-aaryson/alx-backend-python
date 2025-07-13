import sqlite3

class DatabaseConnection:
    """A class-based context manager for database connections"""
    
    def __init__(self, database_name='users.db'):
        self.database_name = database_name
        self.connection = None
        self.cursor = None
    
    def __enter__(self):
        """Open the database connection and return the cursor"""
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

# Use the context manager with the with statement
with DatabaseConnection() as cursor:
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results) 