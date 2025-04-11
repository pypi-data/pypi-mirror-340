"""
Example of handling callbacks from the Atmos API using Flask.

To run this example:
1. Install Flask: pip install flask
2. Run the script: python callback_handler.py
3. The server will listen on http://localhost:5000/atmos/callback
4. You can test it by sending a POST request to this endpoint with the
   expected data
"""

import os
import sys

# Add the parent directory to the path so we can import the atmos package
# Note: This import structure is common in example scripts but would be
# different in a real application where the package is properly installed
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# pylint: disable=wrong-import-position
from flask import Flask, request, jsonify  # noqa
from atmos.utils import validate_callback_signature, create_callback_response  # noqa

app = Flask(__name__)

# Your API key provided by Atmos
API_KEY = "your_api_key"


@app.route('/atmos/callback', methods=['POST'])
def atmos_callback():
    """
    Handle callbacks from the Atmos API.

    Expected data:
    {
        "store_id": "your_store_id",
        "transaction_id": "123456",
        "transaction_time": "2023-01-01T12:00:00",
        "amount": "5000000",
        "invoice": "12345",
        "sign": "md5_hash_of_the_above_data_plus_api_key"
    }
    """
    data = request.json

    # Log the received data
    print(f"Received callback data: {data}")

    # Validate the signature
    if not validate_callback_signature(data, API_KEY):
        print("Invalid signature")
        error_msg = "Invalid signature"
        return jsonify(create_callback_response(False, error_msg)), 400

    # Process the payment
    # Extract payment data (store_id is not used but kept for reference)
    # pylint: disable=unused-variable
    transaction_id = data["transaction_id"]
    transaction_time = data["transaction_time"]
    amount = data["amount"]
    invoice = data["invoice"]

    # Your payment processing logic here
    # For example, update your database to mark the invoice as paid
    print(f"Processing payment for invoice {invoice}")
    print(f"Amount: {int(amount) / 100:.2f}")
    print(f"Transaction ID: {transaction_id}")
    print(f"Transaction time: {transaction_time}")

    # Return a success response
    success_msg = "Payment processed successfully"
    return jsonify(create_callback_response(True, success_msg))


if __name__ == "__main__":
    app.run(debug=True)
    print("Server running on http://localhost:5000/atmos/callback")
