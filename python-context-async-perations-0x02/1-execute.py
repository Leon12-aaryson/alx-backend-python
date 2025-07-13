import sqlite3

class ExecuteQuery:
    """A reusable context manager that takes a query as input and executes it"""
    
    def __init__(self, query, *params):
        self.query = query
        self.params = params
        self.conn = None
        self.cursor = None
        self.result = None
    
    def __enter__(self):
        """Set up the database connection and cursor"""
        self.conn = sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up the database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def execute(self):
        """Execute the query and return the results"""
        self.cursor.execute(self.query, self.params)
        self.result = self.cursor.fetchall()
        return self.result

# Example usage
if __name__ == "__main__":
    with ExecuteQuery("SELECT * FROM users WHERE age > ?", 25) as query_executor:
        results = query_executor.execute()
        print(results) 