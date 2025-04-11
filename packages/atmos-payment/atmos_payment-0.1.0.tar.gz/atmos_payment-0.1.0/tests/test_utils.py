"""
Tests for the Atmos API utilities.
"""

import unittest
import hashlib

from atmos.utils import validate_callback_signature, create_callback_response


class TestUtils(unittest.TestCase):
    """Tests for the utility functions."""
    
    def test_validate_callback_signature(self):
        """Test validating a callback signature."""
        # Create test data
        api_key = "test_api_key"
        store_id = "test_store"
        transaction_id = "123456"
        invoice = "12345"
        amount = "5000000"
        
        # Calculate the expected signature
        sign_string = f"{store_id}{transaction_id}{invoice}{amount}{api_key}"
        expected_sign = hashlib.md5(sign_string.encode()).hexdigest()
        
        # Create the callback data
        data = {
            "store_id": store_id,
            "transaction_id": transaction_id,
            "invoice": invoice,
            "amount": amount,
            "sign": expected_sign
        }
        
        # Validate the signature
        self.assertTrue(validate_callback_signature(data, api_key))
        
        # Test with an invalid signature
        data["sign"] = "invalid_signature"
        self.assertFalse(validate_callback_signature(data, api_key))
        
        # Test with missing fields
        for field in ["store_id", "transaction_id", "invoice", "amount", "sign"]:
            data_copy = data.copy()
            del data_copy[field]
            self.assertFalse(validate_callback_signature(data_copy, api_key))
    
    def test_create_callback_response(self):
        """Test creating a callback response."""
        # Test a success response
        response = create_callback_response(True)
        self.assertEqual(response["status"], 1)
        self.assertEqual(response["message"], "Успешно")
        
        # Test a success response with a custom message
        response = create_callback_response(True, "Payment successful")
        self.assertEqual(response["status"], 1)
        self.assertEqual(response["message"], "Payment successful")
        
        # Test an error response
        response = create_callback_response(False)
        self.assertEqual(response["status"], 0)
        self.assertEqual(response["message"], "Ошибка")
        
        # Test an error response with a custom message
        response = create_callback_response(False, "Invalid invoice")
        self.assertEqual(response["status"], 0)
        self.assertEqual(response["message"], "Invalid invoice")


if __name__ == '__main__':
    unittest.main()
