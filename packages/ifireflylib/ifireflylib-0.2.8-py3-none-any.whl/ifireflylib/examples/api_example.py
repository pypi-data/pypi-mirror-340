#!/usr/bin/env python3
"""
Example usage of the FireflyDB Client

This script demonstrates how to use the FireflyDB client to interact with the Firefly database.
"""

import logging
import sys
from ifireflylib import IFireflyClient

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("FireflyDB.Example")


def main():
    """Main function demonstrating the FireflyDB client"""
    logger.info("Starting FireflyDB client example...")

    try:
        # Create a FireflyDB client instance
        # Replace with your actual server details
        client = IFireflyClient(host="localhost", port=6379, password="xyz123")
        
        # Test the connection
        if not client.ping():
            logger.error("Failed to connect to Firefly server")
            return
        
        logger.info("Connected to Firefly server")
        
        # String operations
        logger.info("\n=== String Operations ===")
        
        # Set a value
        client.string_ops.string_set("greeting", "Hello, Firefly!")
        logger.info("Set 'greeting' to 'Hello, Firefly!'")
        
        # Get a value
        value = client.string_ops.string_get("greeting")
        logger.info(f"Got 'greeting': {value}")
        
        # Delete a key
        count = client.string_ops.delete("greeting")
        logger.info(f"Deleted 'greeting', removed {count} key(s)")
        
        # List operations
        logger.info("\n=== List Operations ===")
        
        # Push values to a list
        client.list_ops.list_right_push("fruits", "apple")
        client.list_ops.list_right_push("fruits", "banana")
        client.list_ops.list_right_push("fruits", "cherry")
        logger.info("Pushed 'apple', 'banana', 'cherry' to 'fruits' list")
        
        # Get a range of elements
        fruits = client.list_ops.list_range("fruits", 0, -1)
        logger.info(f"List 'fruits': {fruits}")
        
        # Pop a value
        fruit = client.list_ops.list_right_pop("fruits")
        logger.info(f"Popped from 'fruits': {fruit}")
        
        # Hash operations
        logger.info("\n=== Hash Operations ===")
        
        # Set a field in a hash
        client.hash_ops.hash_set("user:1", "name", "John Doe")
        client.hash_ops.hash_set("user:1", "email", "john@example.com")
        client.hash_ops.hash_set("user:1", "age", 30)
        logger.info("Set fields in 'user:1' hash")
        
        # Get a field
        name = client.hash_ops.hash_get("user:1", "name")
        logger.info(f"Got 'user:1.name': {name}")
        
        # Get all fields
        user_data = client.hash_ops.hash_get_all("user:1")
        logger.info(f"Got all fields in 'user:1': {user_data}")
        
        # Delete a field
        client.hash_ops.hash_delete("user:1", "age")
        logger.info("Deleted 'user:1.age' field")
        
        # Set multiple fields at once
        client.hash_ops.hash_multi_set("user:2", {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "age": 25
        })
        logger.info("Set multiple fields in 'user:2' hash")

        # Get all fields
        user_data = client.hash_ops.hash_get_all("user:2")
        logger.info(f"Got all fields in 'user:2': {user_data}")
        
        # Cleanup
        logger.info("\n=== Cleanup ===")
        client.string_ops.delete("fruits")
        client.string_ops.delete("user:1")
        client.string_ops.delete("user:2")
        logger.info("Cleaned up all test keys")
        
    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        logger.info("Example completed")


if __name__ == "__main__":
    main() 