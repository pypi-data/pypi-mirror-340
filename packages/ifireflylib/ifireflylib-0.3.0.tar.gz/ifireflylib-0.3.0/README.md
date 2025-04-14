# FireflyDB Python Client

A Python client library for the FireflyDB database.

## Features

- Connect to FireflyDB servers
- String operations (get, set, delete)
- List operations (push, pop, range)
- Hash operations (hget, hset, hdel)
- Comprehensive error handling
- Logging support

## Installation

### Prerequisites

- Python 3.13 or higher
- FireflyDB server

### Building from Source

1. Clone the repository:
   ```
   git clone https://gitea.innovativedevsolutions.org/IDSolutions/firefly.git
   cd firefly/ifireflylib
   ```

2. Run the build script:
   ```
   python build.py
   ```

   This will:
   - Check for the native library
   - Build the Python package
   - Optionally install the package in development mode

### Installing with pip

```
pip install ifireflylib
```

## Usage

```python
from ifireflylib import IFireflyClient

# Create a client
client = IFireflyClient(host="localhost", port=6379, password="yourpassword")

# Test the connection
if client.ping():
    print("Connected to Firefly server")
    
    # String operations
    client.string_ops.string_set("greeting", "Hello, Firefly!")
    value = client.string_ops.string_get("greeting")
    print(f"Got 'greeting': {value}")
    
    # List operations
    client.list_ops.list_right_push("fruits", "apple")
    client.list_ops.list_right_push("fruits", "banana")
    fruits = client.list_ops.list_range("fruits", 0, -1)
    print(f"List 'fruits': {fruits}")
    
    # Hash operations
    client.hash_ops.hash_set("user:1", "name", "John Doe")
    name = client.hash_ops.hash_get("user:1", "name")
    print(f"Got 'user:1.name': {name}")
    
    # Clean up
    client.string_ops.delete("greeting")
    client.string_ops.delete("fruits")
    client.string_ops.delete("user:1")
    
    # Close the connection
    client.close()
```

## License

MIT License