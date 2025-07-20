# Unit Testing and Integration Testing

This project focuses on implementing unit tests and integration tests for Python code, covering testing patterns such as mocking, parametrization, and fixtures.

## Learning Objectives

At the end of this project, you will be able to explain to anyone, without the help of Google:

- The difference between unit and integration tests
- Common testing patterns such as mocking, parametrizations and fixtures

## Project Structure

```text
0x03-Unittests_and_integration_tests/
├── README.md
├── utils.py
├── test_utils.py
├── client.py
└── fixtures.py
```

## Files Description

### `utils.py`

Contains utility functions for the GitHub organization client:

- `access_nested_map()`: Access nested map with key path
- `get_json()`: Get JSON from remote URL
- `memoize()`: Decorator to memoize a method

### `test_utils.py`

Contains unit tests for the utils module:

- `TestAccessNestedMap`: Test cases for the `access_nested_map` function

  - `test_access_nested_map()`: Tests successful access to nested maps
  - `test_access_nested_map_exception()`: Tests KeyError exceptions for invalid paths

### `client.py`

Contains the `GithubOrgClient` class for interacting with GitHub API:

- `org()`: Get organization information
- `repos_payload()`: Get repositories payload
- `public_repos()`: Get public repository names

### `fixtures.py`

Contains test fixtures and mock data for GitHub API responses.

## Testing

### Running Tests

To run the unit tests:

```bash
python -m unittest test_utils.py
```

To run tests with verbose output:

```bash
python -m unittest test_utils.py -v
```

### Test Coverage

The tests cover:

- **Unit Tests**: Testing individual functions in isolation
- **Parameterized Tests**: Using `@parameterized.expand` to test multiple inputs
- **Exception Testing**: Using `assertRaises` to test error conditions
- **Mocking**: Mocking external dependencies (network calls, database access)

## Requirements

- Python 3.7+
- `parameterized` package for parameterized testing
- `requests` package for HTTP requests
- `pycodestyle` for code style checking

## Installation

```bash
# Install required packages
pip install parameterized requests pycodestyle

# Make files executable
chmod +x *.py
```

## Code Style

All code follows the pycodestyle (PEP 8) guidelines. To check code style:

```bash
pycodestyle *.py
```

## Documentation

All modules, classes, and functions include proper documentation that can be accessed via:

```bash
python3 -c 'print(__import__("module_name").__doc__)'
python3 -c 'print(__import__("module_name").ClassName.__doc__)'
python3 -c 'print(__import__("module_name").function_name.__doc__)'
```

## Testing Patterns

### Unit Testing

- Tests individual functions in isolation
- Mocks external dependencies
- Tests standard inputs and corner cases
- Answers: "If everything outside this function works, does this function work?"

### Integration Testing

- Tests code paths end-to-end
- Only mocks low-level external calls (HTTP, file I/O, database I/O)
- Tests interactions between all parts of the code

### Parameterized Testing

- Uses `@parameterized.expand` decorator
- Tests multiple input combinations efficiently
- Reduces code duplication in test methods

### Mocking

- Replaces external dependencies with controlled test doubles
- Ensures tests are fast and reliable
- Prevents tests from making actual network or database calls 