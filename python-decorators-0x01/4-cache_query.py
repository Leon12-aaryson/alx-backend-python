import time
import sqlite3 
import functools

query_cache = {}

def with_db_connection(func):
    """Decorator that automatically handles opening and closing database connections"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def cache_query(func):
    """Decorator that caches query results based on the SQL query string"""
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Try to get the query from kwargs or args
        query = kwargs.get('query')
        if query is None and len(args) > 0:
            query = args[0] if isinstance(args[0], str) else None
        if query is None and len(args) > 1:
            query = args[1] if isinstance(args[1], str) else None
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        print(f"Cache miss for query: {query}. Executing and caching result.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users") 