# Python Generators - MySQL Database Streaming

This project implements Python generators to stream data from a MySQL database efficiently. The main objective is to create a generator that streams rows from an SQL database one by one, avoiding loading all data into memory at once.

## Project Structure

```
python-generators-0x00/
├── README.md                   # This file
├── seed.py                     # Database setup and seeding script
├── 0-stream_users.py          # Generator for streaming users
├── 0-main.py                  # Test script
├── user_data.csv              # Sample data file
├── 1-batch_processing.py      # Batch processing generator
├── 2-lazy_paginate.py         # Lazy pagination generator
└── 4-stream_ages.py           # Stream ages generator
```

## Requirements

- Python 3.x
- MySQL Server
- mysql-connector-python

## Installation

1. Install MySQL Server on your system
2. Install the required Python package:
   ```bash
   pip install mysql-connector-python
   ```

## Database Setup

The project uses a MySQL database with the following specifications:

### Database: `ALX_prodev`
### Table: `user_data`

| Field   | Type        | Description                    |
|---------|-------------|--------------------------------|
| user_id | CHAR(36)    | Primary Key, UUID, Indexed     |
| name    | VARCHAR(255)| NOT NULL                       |
| email   | VARCHAR(255)| NOT NULL                       |
| age     | DECIMAL(3,0)| NOT NULL                       |

## Files Description

### seed.py
Main database seeding script that contains the following functions:

- `connect_db()`: Connects to the MySQL database server
- `create_database(connection)`: Creates the database ALX_prodev if it does not exist
- `connect_to_prodev()`: Connects to the ALX_prodev database in MySQL
- `create_table(connection)`: Creates the user_data table if it does not exist
- `insert_data(connection, data)`: Inserts data from CSV file into the database
- `stream_users()`: Generator that streams users from the database

### 0-stream_users.py
Contains generators for streaming user data:

- `stream_users()`: Generator that yields individual user records
- `stream_users_in_batches(batch_size)`: Generator that yields batches of user records

### user_data.csv
Sample CSV file containing user data with the following format:
```
user_id,name,email,age
00234e50-34eb-4ce2-94ec-26e3fa749796,Dan Altenwerth Jr.,Molly59@gmail.com,67
...
```

## Usage

### 1. Database Setup and Seeding

```bash
# Run the seeding script
python3 seed.py
```

Or use the test script:
```bash
python3 0-main.py
```

### 2. Streaming Users

```python
from seed import stream_users

# Stream users one by one
for user in stream_users():
    print(user)
```

### 3. Using the Generator Module

```python
from 0-stream_users import stream_users, stream_users_in_batches

# Stream individual users
for user in stream_users():
    print(user)

# Stream users in batches
for batch in stream_users_in_batches(batch_size=100):
    print(f"Processing batch of {len(batch)} users")
    for user in batch:
        process_user(user)
```

## Configuration

Before running the scripts, update the database connection parameters in both `seed.py` and `0-stream_users.py`:

```python
connection = mysql.connector.connect(
    host='localhost',
    user='your_username',      # Change this
    password='your_password',  # Change this
    database='ALX_prodev'
)
```

## Expected Output

When running the test script (`0-main.py`), you should see output similar to:
```
connection successful
Table user_data created successfully
Database ALX_prodev is present 
[('00234e50-34eb-4ce2-94ec-26e3fa749796', 'Dan Altenwerth Jr.', 'Molly59@gmail.com', 67), ...]
```

## Benefits of Using Generators

1. **Memory Efficiency**: Only one row is loaded into memory at a time
2. **Lazy Evaluation**: Data is processed on-demand
3. **Scalability**: Can handle large datasets without memory issues
4. **Stream Processing**: Enables real-time data processing

## Error Handling

The generators include proper error handling for:
- Database connection failures
- Query execution errors
- Resource cleanup (connections and cursors)

## Repository Information

- **GitHub repository**: alx-backend-python
- **Directory**: python-generators-0x00
- **Files**: seed.py, README.md, 0-stream_users.py

## License

This project is part of the ALX Backend Python curriculum.
