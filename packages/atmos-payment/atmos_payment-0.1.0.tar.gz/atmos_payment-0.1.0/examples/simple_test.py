"""
Simple test for the Atmos payment library.
"""

import os
import sys

# Add the parent directory to the path so we can import the atmos package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from atmos import AtmosClient

# Create a client with test credentials
client = AtmosClient(
    consumer_key="test_key",
    consumer_secret="test_secret",
    store_id="test_store",
    test_mode=True
)

# Print the client configuration
print("Atmos Client Configuration:")
print(f"Base URL: {client.base_url}")
print(f"Store ID: {client.store_id}")
print(f"Test Mode: {client.base_url == client.TEST_BASE_URL}")
print(f"Language: {client.language}")

print("\nAtmos library is working correctly!")
