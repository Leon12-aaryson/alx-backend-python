# Python Generators - MySQL Database Streaming

This project implements Python generators to stream data from a MySQL database efficiently. The main objective is to create a generator that streams rows from an SQL database one by one, avoiding loading all data into memory at once.

## Project Structure

```
python-generators-0x00/
├── README.md                   # This file
├── seed.py                     # Database setup and seeding script
├── 0-stream_users.py          # Generator for streaming users
├── 0-main.py                  # Test script for seed functionality
├── user_data.csv              # Sample data file
├── 1-batch_processing.py      # Batch processing generator
├── 2-main.py                  # Test script for batch processing
├── 2-lazy_paginate.py         # Lazy pagination generator
├── 3-main.py                  # Test script for lazy pagination
├── 4-stream_ages.py           # Stream ages generator
└── test_all_generators.py     # Comprehensive test script
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

### 1-batch_processing.py

Contains generators for batch processing large datasets:

- `stream_users_in_batches(batch_size)`: Generator that fetches users in batches
- `batch_processing(batch_size)`: Processes each batch to filter users over age 25
- Uses exactly 3 loops as required
- Memory-efficient batch processing for large datasets

### 2-lazy_paginate.py

Implements lazy loading for paginated data:

- `paginate_users(page_size, offset)`: Fetches a specific page of users
- `lazy_paginate(page_size)`: Generator that lazily loads pages only when needed
- Uses only 1 loop as required
- Efficient for processing large datasets without loading everything into memory

### 4-stream_ages.py

Memory-efficient aggregation using generators:

- `stream_user_ages()`: Generator that yields user ages one by one
- `calculate_average_age()`: Calculates average age without loading entire dataset
- Uses exactly 2 loops as required
- Does not use SQL AVERAGE function, computes in Python

### test_all_generators.py

Comprehensive test script that demonstrates all generator patterns with mock data.

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

### 4. Batch Processing

```python
from 1-batch_processing import stream_users_in_batches, batch_processing

# Process users in batches of 50, filtering age > 25
batch_processing(50)

# Or use the generator directly
for batch in stream_users_in_batches(100):
    print(f"Processing batch of {len(batch)} users")
    for user in batch:
        if user['age'] > 25:
            print(f"  - {user['name']} (Age: {user['age']})")
```

### 5. Lazy Pagination

```python
from 2-lazy_paginate import lazy_paginate

# Lazily load pages of 100 users each
for page_num, page in enumerate(lazy_paginate(100), 1):
    print(f"Page {page_num}: {len(page)} users")
    for user in page:
        print(f"  - {user['name']}")
```

### 6. Memory-Efficient Aggregation

```python
from 4-stream_ages import stream_user_ages, calculate_average_age

# Calculate average age efficiently
average = calculate_average_age()

# Or use the generator directly
total_age = 0
count = 0
for age in stream_user_ages():
    total_age += age
    count += 1
print(f"Average age: {total_age / count}")
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
