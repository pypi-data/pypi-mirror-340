"""
Tests for the Atmos API client.
"""

import unittest
from unittest.mock import patch, MagicMock

from atmos import AtmosClient, AtmosAPIError, AtmosAuthError
from atmos.models import OfdItem, Transaction


# pylint: disable=protected-access
# Note: In unit tests, it's acceptable to access protected members

class TestAtmosClient(unittest.TestCase):
    """Tests for the AtmosClient class."""

    def setUp(self):
        """Set up the test case."""
        self.client = AtmosClient(
            consumer_key="test_key",
            consumer_secret="test_secret",
            store_id="test_store",
            test_mode=True
        )

    @patch('atmos.client.requests.post')
    def test_get_token(self, mock_post):
        """Test getting an access token."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_token",
            "expires_in": 3600
        }
        mock_post.return_value = mock_response

        # Call the method
        token = self.client._get_token()

        # Check the result
        self.assertEqual(token, "test_token")
        self.assertEqual(self.client.access_token, "test_token")

        # Check that the request was made correctly
        mock_post.assert_called_once()
        _, kwargs = mock_post.call_args
        content_type = kwargs["headers"]["Content-Type"]
        self.assertEqual(content_type, "application/x-www-form-urlencoded")
        auth = kwargs["headers"]["Authorization"]
        self.assertTrue(auth.startswith("Basic "))
        self.assertEqual(kwargs["data"]["grant_type"], "client_credentials")

    @patch('atmos.client.requests.post')
    def test_get_token_error(self, mock_post):
        """Test getting an access token with an error."""
        # Mock the response
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response

        # Call the method and check the exception
        with self.assertRaises(AtmosAuthError):
            self.client._get_token()

    @patch('atmos.client.requests.request')
    @patch('atmos.client.AtmosClient._ensure_token')
    def test_request(self, mock_ensure_token, mock_request):
        """Test making a request to the API."""
        # Mock the token
        mock_ensure_token.return_value = "test_token"

        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": {
                "code": "OK",
                "description": "No errors"
            },
            "data": "test_data"
        }
        mock_request.return_value = mock_response

        # Call the method
        result = self.client._request("POST", "/test", {"key": "value"})

        # Check the result
        self.assertEqual(result["data"], "test_data")

        # Check that the request was made correctly
        mock_request.assert_called_once()
        _, kwargs = mock_request.call_args
        self.assertEqual(kwargs["method"], "POST")
        self.assertEqual(kwargs["url"], "https://test-partner.atmos.uz/test")
        content_type = kwargs["headers"]["Content-Type"]
        self.assertEqual(content_type, "application/json")
        auth = kwargs["headers"]["Authorization"]
        self.assertEqual(auth, "Bearer test_token")
        self.assertEqual(kwargs["json"], {"key": "value"})

    @patch('atmos.client.requests.request')
    @patch('atmos.client.AtmosClient._ensure_token')
    def test_request_error(self, mock_ensure_token, mock_request):
        """Test making a request to the API with an error."""
        # Mock the token
        mock_ensure_token.return_value = "test_token"

        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "result": {
                "code": "STPIMS-ERR-001",
                "description": "Internal error"
            }
        }
        mock_request.return_value = mock_response

        # Call the method and check the exception
        with self.assertRaises(AtmosAPIError) as context:
            self.client._request("POST", "/test")

        # Check the exception details
        self.assertEqual(context.exception.code, "STPIMS-ERR-001")
        self.assertEqual(context.exception.message, "Internal error")

    @patch('atmos.client.AtmosClient._request')
    def test_create_transaction(self, mock_request):
        """Test creating a transaction."""
        # Mock the response
        mock_request.return_value = {
            "result": {
                "code": "OK",
                "description": "No errors"
            },
            "transaction_id": 123456,
            "store_transaction": {
                "trans_id": 123456,
                "account": "12345",
                "amount": 5000000,
                "terminal_id": "test_terminal",
                "confirmed": False,
                "total": 5000000
            }
        }

        # Call the method
        result = self.client.create_transaction(
            amount=5000000,
            account="12345",
            terminal_id="test_terminal"
        )

        # Check the result
        self.assertEqual(result.transaction_id, 123456)
        self.assertEqual(result.store_transaction.amount, 5000000)

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/pay/create")
        self.assertEqual(args[2]["amount"], 5000000)
        self.assertEqual(args[2]["account"], "12345")
        self.assertEqual(args[2]["terminal_id"], "test_terminal")
        self.assertEqual(args[2]["store_id"], "test_store")

    @patch('atmos.client.AtmosClient._request')
    def test_create_ofd_transaction(self, mock_request):
        """Test creating an OFD transaction."""
        # Mock the response
        mock_request.return_value = {
            "result": {
                "code": "OK",
                "description": "No errors"
            },
            "transaction_id": 123456,
            "store_transaction": {
                "trans_id": 123456,
                "account": "12345",
                "amount": 5000000,
                "terminal_id": "test_terminal",
                "confirmed": False,
                "total": 5000000
            }
        }

        # Create OFD items
        ofd_items = [
            OfdItem(
                ofd_code="123456789",
                name="Product 1",
                amount=3000000,
                quantity=1
            ),
            OfdItem(
                ofd_code="987654321",
                name="Product 2",
                amount=2000000,
                quantity=2
            )
        ]

        # Call the method
        result = self.client.create_ofd_transaction(
            amount=5000000,
            account="12345",
            ofd_items=ofd_items
        )

        # Check the result
        self.assertEqual(result.transaction_id, 123456)

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/pay/create/checkout-ofd")
        self.assertEqual(args[2]["amount"], 5000000)
        self.assertEqual(args[2]["account"], "12345")
        self.assertEqual(len(args[2]["ofd_items"]), 2)
        ofd_code = args[2]["ofd_items"][0]["ofd_code"]
        self.assertEqual(ofd_code, "123456789")
        self.assertEqual(args[2]["ofd_items"][0]["amount"], 3000000)

    @patch('atmos.client.AtmosClient._request')
    def test_pre_confirm_transaction(self, mock_request):
        """Test pre-confirming a transaction."""
        # Mock the response
        mock_request.return_value = {
            "result": {
                "code": "OK",
                "description": "No errors"
            }
        }

        # Call the method with a card number
        result = self.client.pre_confirm_transaction(
            transaction_id=123456,
            card_number="8600490744313347",
            expiry="2410"
        )

        # Check the result
        self.assertTrue(result)

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/pay/pre-apply")
        self.assertEqual(args[2]["transaction_id"], 123456)
        self.assertEqual(args[2]["card_number"], "8600490744313347")
        self.assertEqual(args[2]["expiry"], "2410")

        # Reset the mock
        mock_request.reset_mock()

        # Call the method with a card token
        result = self.client.pre_confirm_transaction(
            transaction_id=123456,
            card_token="test_token"
        )

        # Check the result
        self.assertTrue(result)

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[2]["transaction_id"], 123456)
        self.assertEqual(args[2]["card_token"], "test_token")
        self.assertNotIn("card_number", args[2])
        self.assertNotIn("expiry", args[2])

    @patch('atmos.client.AtmosClient._request')
    def test_confirm_transaction(self, mock_request):
        """Test confirming a transaction."""
        # Mock the response
        mock_request.return_value = {
            "result": {
                "code": "OK",
                "description": "No errors"
            },
            "store_transaction": {
                "success_trans_id": 654321,
                "trans_id": 123456,
                "account": "12345",
                "amount": 5000000,
                "terminal_id": "test_terminal",
                "confirmed": True,
                "total": 5000000,
                "card_id": "test_token",
                "status_code": "0",
                "status_message": "Success"
            }
        }

        # Call the method
        result = self.client.confirm_transaction(
            transaction_id=123456,
            otp="111111"
        )

        # Check the result
        self.assertEqual(result.store_transaction.trans_id, 123456)
        self.assertTrue(result.store_transaction.confirmed)

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/pay/apply")
        self.assertEqual(args[2]["transaction_id"], 123456)
        self.assertEqual(args[2]["otp"], "111111")
        self.assertEqual(args[2]["store_id"], "test_store")

    @patch('atmos.client.AtmosClient._request')
    def test_create_multi_transaction(self, mock_request):
        """Test creating multiple transactions."""
        # Mock the response
        mock_request.return_value = {
            "result": {
                "code": "OK",
                "description": "No errors"
            },
            "transaction_id": [123456, 123457],
            "store_transactions": [
                {
                    "trans_id": 123456,
                    "account": "user_1",
                    "amount": 50000,
                    "terminal_id": "test_terminal",
                    "confirmed": False,
                    "total": 50000
                },
                {
                    "trans_id": 123457,
                    "account": "user_2",
                    "amount": 100000,
                    "terminal_id": "test_terminal",
                    "confirmed": False,
                    "total": 100000
                }
            ]
        }

        # Create transaction objects
        transactions = [
            Transaction(
                account="user_1",
                amount=50000,
                details="For service 1"
            ),
            Transaction(
                account="user_2",
                amount=100000,
                details="For service 2"
            )
        ]

        # Call the method
        result = self.client.create_multi_transaction(transactions)

        # Check the result
        self.assertEqual(result.transaction_id, [123456, 123457])

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/bulk/pay/create")
        self.assertEqual(args[2]["store_id"], "test_store")
        self.assertEqual(len(args[2]["params"]), 2)
        self.assertEqual(args[2]["params"][0]["account"], "user_1")
        self.assertEqual(args[2]["params"][0]["amount"], 50000)
        self.assertEqual(args[2]["params"][1]["account"], "user_2")
        self.assertEqual(args[2]["params"][1]["amount"], 100000)


if __name__ == '__main__':
    unittest.main()
