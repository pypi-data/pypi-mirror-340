"""
Example of generating a payment page URL using the Atmos API.
"""

import os
import sys
import time

# Add the parent directory to the path so we can import the atmos package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from atmos import AtmosClient, AtmosAPIError


def main():
    # Initialize the client with your credentials
    client = AtmosClient(
        consumer_key="your_consumer_key",
        consumer_secret="your_consumer_secret",
        store_id="your_store_id",
        test_mode=True  # Use the test environment
    )
    
    try:
        # Create a transaction
        print("Creating transaction...")
        transaction = client.create_transaction(
            amount=5000000,  # 50,000.00 currency units
            account="12345",  # Your internal payment identifier
        )
        
        transaction_id = transaction.transaction_id
        print(f"Transaction created with ID: {transaction_id}")
        
        # Get the payment page URL
        payment_url = client.get_test_payment_page_url(
            transaction_id=transaction_id,
            redirect_url="https://your-website.com/payment/success"
        )
        
        print(f"Payment page URL: {payment_url}")
        print("In a real application, you would redirect the user to this URL.")
        print("After the payment is completed, the user will be redirected to your redirect URL.")
        
    except AtmosAPIError as e:
        print(f"API error: {e.code} - {e.message}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
