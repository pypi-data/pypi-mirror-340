"""
Test the Atmos callback handler functionality.

This script simulates an Atmos callback and tests the callback validation
and response generation utilities.
"""

import os
import sys
import hashlib
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time
import requests

# Add the parent directory to the path so we can import the atmos package
# Note: This import structure is common in example scripts but would be
# different in a real application where the package is properly installed
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# pylint: disable=wrong-import-position
from atmos.utils import validate_callback_signature, create_callback_response  # noqa


# Test API key for signature validation
TEST_API_KEY = "test_api_key"

# Test callback data
TEST_CALLBACK_DATA = {
    "store_id": "test_store",
    "transaction_id": "123456",
    "transaction_time": "2023-01-01T12:00:00",
    "amount": "5000000",
    "invoice": "12345"
}


def generate_signature(data, api_key):
    """Generate a signature for the callback data."""
    sign_parts = [
        data['store_id'],
        data['transaction_id'],
        data['invoice'],
        data['amount'],
        api_key
    ]
    sign_string = "".join(sign_parts)
    return hashlib.md5(sign_string.encode()).hexdigest()


class CallbackHandler(BaseHTTPRequestHandler):
    """HTTP handler for testing callbacks."""

    # pylint: disable=invalid-name
    # Note: do_POST is a required method name for BaseHTTPRequestHandler
    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        print(f"Received callback data: {data}")

        # Validate the signature
        if not validate_callback_signature(data, TEST_API_KEY):
            print("Invalid signature")
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = create_callback_response(False, "Invalid signature")
            self.wfile.write(json.dumps(response).encode())
            return

        # Process the payment
        # Extract payment data
        transaction_id = data["transaction_id"]
        transaction_time = data["transaction_time"]
        amount = data["amount"]
        invoice = data["invoice"]

        # Your payment processing logic here
        print(f"Processing payment for invoice {invoice}")
        print(f"Amount: {int(amount) / 100:.2f}")
        print(f"Transaction ID: {transaction_id}")
        print(f"Transaction time: {transaction_time}")

        # Return a success response
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        success_msg = "Payment processed successfully"
        response = create_callback_response(True, success_msg)
        self.wfile.write(json.dumps(response).encode())


def run_server(port=8000):
    """Run the test server."""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CallbackHandler)
    print(f"Starting server on port {port}...")
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    return httpd


def test_valid_callback():
    """Test a valid callback."""
    # Create a copy of the test data
    data = TEST_CALLBACK_DATA.copy()

    # Generate a valid signature
    data["sign"] = generate_signature(data, TEST_API_KEY)

    # Send the callback
    response = requests.post(
        "http://localhost:8000/callback",
        json=data,
        timeout=5
    )

    # Check the response
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")

    # Verify the response
    assert response.status_code == 200
    assert response.json()["status"] == 1

    print("Valid callback test passed!")


def test_invalid_callback():
    """Test an invalid callback."""
    # Create a copy of the test data
    data = TEST_CALLBACK_DATA.copy()

    # Generate an invalid signature
    data["sign"] = "invalid_signature"

    # Send the callback
    response = requests.post(
        "http://localhost:8000/callback",
        json=data,
        timeout=5
    )

    # Check the response
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")

    # Verify the response
    assert response.status_code == 400
    assert response.json()["status"] == 0

    print("Invalid callback test passed!")


def test_missing_fields():
    """Test a callback with missing fields."""
    # Create a copy of the test data with a missing field
    data = TEST_CALLBACK_DATA.copy()

    # Add a signature first (based on complete data)
    complete_data = data.copy()
    complete_data["sign"] = generate_signature(complete_data, TEST_API_KEY)

    # Now remove a field
    del data["invoice"]
    data["sign"] = complete_data["sign"]

    # Send the callback
    response = requests.post(
        "http://localhost:8000/callback",
        json=data,
        timeout=5
    )

    # Check the response
    print(f"Response status code: {response.status_code}")
    print(f"Response body: {response.json()}")

    # Verify the response
    assert response.status_code == 400
    assert response.json()["status"] == 0

    print("Missing fields test passed!")


def main():
    """Run the tests."""
    # Start the server
    httpd = run_server()

    try:
        # Wait for the server to start
        time.sleep(1)

        print("\n=== Testing Atmos Callback Handler ===\n")

        # Test a valid callback
        print("\n--- Testing Valid Callback ---")
        test_valid_callback()

        # Test an invalid callback
        print("\n--- Testing Invalid Callback ---")
        test_invalid_callback()

        # Test a callback with missing fields
        print("\n--- Testing Callback with Missing Fields ---")
        test_missing_fields()

        print("\n=== All tests passed! ===")

    except (ConnectionError, TimeoutError) as e:
        print(f"Connection error: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except KeyError as e:
        print(f"Key error: {e}")
    finally:
        # Shutdown the server
        httpd.shutdown()
        print("Server shutdown")


if __name__ == "__main__":
    main()
