"""
Mock test for the Atmos payment library.

This script demonstrates how to use the Atmos library with mocks,
allowing you to test your integration without making actual API calls.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the atmos package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from atmos import AtmosClient, OfdItem, Transaction, AtmosAPIError


class MockTest(unittest.TestCase):
    """Test the Atmos library with mocks."""

    def setUp(self):
        """Set up the test case."""
        # Create a client with test credentials
        self.client = AtmosClient(
            consumer_key="test_key",
            consumer_secret="test_secret",
            store_id="test_store",
            test_mode=True
        )

    @patch('atmos.client.requests.post')
    def test_authentication(self, mock_post):
        """Test authentication."""
        # Mock the token response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": "test_token",
            "scope": "am_application_scope default",
            "token_type": "Bearer",
            "expires_in": 3600
        }
        mock_post.return_value = mock_response

        # Get the token
        token = self.client._get_token()

        # Check the result
        self.assertEqual(token, "test_token")
        print("✅ Authentication successful")

        # Check that the request was made correctly
        mock_post.assert_called_once()
        # The URL is passed as the first positional argument
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].endswith("/token"))
        self.assertEqual(kwargs["headers"]["Content-Type"], "application/x-www-form-urlencoded")
        self.assertTrue(kwargs["headers"]["Authorization"].startswith("Basic "))
        self.assertEqual(kwargs["data"], {"grant_type": "client_credentials"})
        print("✅ Authentication request was correct")

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

        # Create a transaction
        transaction = self.client.create_transaction(
            amount=5000000,
            account="12345",
            terminal_id="test_terminal"
        )

        # Check the result
        self.assertEqual(transaction.transaction_id, 123456)
        self.assertEqual(transaction.store_transaction.amount, 5000000)
        print("✅ Transaction created successfully")

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/pay/create")
        print("✅ Transaction request was correct")

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

        # Pre-confirm the transaction
        result = self.client.pre_confirm_transaction(
            transaction_id=123456,
            card_number="8600490744313347",
            expiry="2410"
        )

        # Check the result
        self.assertTrue(result)
        print("✅ Transaction pre-confirmed successfully")

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/pay/pre-apply")
        print("✅ Pre-confirmation request was correct")

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

        # Confirm the transaction
        result = self.client.confirm_transaction(
            transaction_id=123456,
            otp="111111"
        )

        # Check the result
        self.assertEqual(result.store_transaction.trans_id, 123456)
        self.assertTrue(result.store_transaction.confirmed)
        print("✅ Transaction confirmed successfully")

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/pay/apply")
        print("✅ Confirmation request was correct")

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
                "amount": 500000,
                "terminal_id": "test_terminal",
                "confirmed": False,
                "total": 500000
            }
        }

        # Create OFD items
        ofd_items = [
            OfdItem(
                ofd_code="123456789",
                name="Product 1",
                amount=300000,
                quantity=1
            ),
            OfdItem(
                ofd_code="987654321",
                name="Product 2",
                amount=200000,
                quantity=1
            )
        ]

        # Create an OFD transaction
        transaction = self.client.create_ofd_transaction(
            amount=500000,
            account="12345",
            ofd_items=ofd_items
        )

        # Check the result
        self.assertEqual(transaction.transaction_id, 123456)
        print("✅ OFD transaction created successfully")

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/pay/create/checkout-ofd")
        print("✅ OFD transaction request was correct")

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

        # Create multiple transactions
        result = self.client.create_multi_transaction(transactions)

        # Check the result
        self.assertEqual(result.transaction_id, [123456, 123457])
        print("✅ Multiple transactions created successfully")

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/bulk/pay/create")
        print("✅ Multiple transactions request was correct")

    @patch('atmos.client.AtmosClient._request')
    def test_request_card_binding(self, mock_request):
        """Test requesting a card binding."""
        # Mock the response
        mock_request.return_value = {
            "result": {
                "code": "OK",
                "description": "No errors"
            },
            "binding_id": 123456
        }

        # Request a card binding
        result = self.client.request_card_binding(
            card_number="8600490744313347",
            expiry="2410",
            phone="+998901234567"
        )

        # Check the result
        self.assertEqual(result["binding_id"], 123456)
        print("✅ Card binding requested successfully")

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/card/bind")
        print("✅ Card binding request was correct")

    @patch('atmos.client.AtmosClient._request')
    def test_confirm_card_binding(self, mock_request):
        """Test confirming a card binding."""
        # Mock the response
        mock_request.return_value = {
            "result": {
                "code": "OK",
                "description": "No errors"
            },
            "card_token": "test_token"
        }

        # Confirm a card binding
        result = self.client.confirm_card_binding(
            binding_id=123456,
            otp="111111"
        )

        # Check the result
        self.assertEqual(result["card_token"], "test_token")
        print("✅ Card binding confirmed successfully")

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/card/bind/confirm")
        print("✅ Card binding confirmation request was correct")

    @patch('atmos.client.AtmosClient._request')
    def test_get_bound_cards(self, mock_request):
        """Test getting bound cards."""
        # Mock the response
        mock_request.return_value = {
            "result": {
                "code": "OK",
                "description": "No errors"
            },
            "cards": [
                {
                    "token": "token1",
                    "masked_pan": "860049******3347",
                    "expiry": "2410",
                    "card_type": "UZCARD",
                    "status": True
                },
                {
                    "token": "token2",
                    "masked_pan": "986009******1907",
                    "expiry": "2505",
                    "card_type": "HUMO",
                    "status": True
                }
            ]
        }

        # Get bound cards
        cards = self.client.get_bound_cards()

        # Check the result
        self.assertEqual(len(cards), 2)
        self.assertEqual(cards[0].token, "token1")
        self.assertEqual(cards[0].masked_pan, "860049******3347")
        self.assertEqual(cards[1].token, "token2")
        self.assertEqual(cards[1].masked_pan, "986009******1907")
        print("✅ Bound cards retrieved successfully")

        # Check that the request was made correctly
        mock_request.assert_called_once()
        args, _ = mock_request.call_args
        self.assertEqual(args[0], "POST")
        self.assertEqual(args[1], "/merchant/card/list")
        print("✅ Get bound cards request was correct")

    @patch('atmos.client.AtmosClient._request')
    def test_error_handling(self, mock_request):
        """Test error handling."""
        # Mock an error response
        mock_request.return_value = {
            "result": {
                "code": "STPIMS-ERR-057",
                "description": "Insufficient funds"
            }
        }

        # Try to create a transaction and expect an error
        try:
            self.client.create_transaction(
                amount=5000000,
                account="12345"
            )
            self.fail("Expected an AtmosAPIError")
        except AtmosAPIError as e:
            self.assertEqual(e.code, "STPIMS-ERR-057")
            self.assertEqual(e.message, "Insufficient funds")
            print("✅ Error handling works correctly")


def run_tests():
    """Run the mock tests."""
    # Create a test suite
    suite = unittest.TestSuite()

    # Add the tests
    suite.addTest(MockTest('test_authentication'))
    suite.addTest(MockTest('test_create_transaction'))
    suite.addTest(MockTest('test_pre_confirm_transaction'))
    suite.addTest(MockTest('test_confirm_transaction'))
    suite.addTest(MockTest('test_create_ofd_transaction'))
    suite.addTest(MockTest('test_create_multi_transaction'))
    suite.addTest(MockTest('test_request_card_binding'))
    suite.addTest(MockTest('test_confirm_card_binding'))
    suite.addTest(MockTest('test_get_bound_cards'))
    suite.addTest(MockTest('test_error_handling'))

    # Run the tests
    runner = unittest.TextTestRunner()
    runner.run(suite)


def simulate_payment_flow():
    """Simulate a complete payment flow with mocks."""
    print("\n=== Simulating a complete payment flow ===\n")

    # Create a client
    client = AtmosClient(
        consumer_key="test_key",
        consumer_secret="test_secret",
        store_id="test_store",
        test_mode=True
    )

    # Mock the _request method
    original_request = client._request

    def mock_request(method, endpoint, data=None, params=None):
        """Mock the _request method."""
        print(f"Making {method} request to {endpoint}")
        print(f"Data: {data}")

        if endpoint == "/merchant/pay/create":
            return {
                "result": {
                    "code": "OK",
                    "description": "No errors"
                },
                "transaction_id": 123456,
                "store_transaction": {
                    "trans_id": 123456,
                    "account": data["account"],
                    "amount": data["amount"],
                    "terminal_id": data.get("terminal_id", "default_terminal"),
                    "confirmed": False,
                    "total": data["amount"]
                }
            }
        elif endpoint == "/merchant/pay/pre-apply":
            return {
                "result": {
                    "code": "OK",
                    "description": "No errors"
                }
            }
        elif endpoint == "/merchant/pay/apply":
            return {
                "result": {
                    "code": "OK",
                    "description": "No errors"
                },
                "store_transaction": {
                    "success_trans_id": 654321,
                    "trans_id": data["transaction_id"],
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

        return original_request(method, endpoint, data, params)

    # Replace the _request method with our mock
    client._request = mock_request

    try:
        # Step 1: Create a transaction
        print("Step 1: Creating a transaction")
        transaction = client.create_transaction(
            amount=5000000,
            account="12345",
            terminal_id="test_terminal"
        )
        print(f"Transaction created with ID: {transaction.transaction_id}")
        print(f"Amount: {transaction.store_transaction.amount / 100:.2f}")

        # Step 2: Pre-confirm the transaction
        print("\nStep 2: Pre-confirming the transaction")
        client.pre_confirm_transaction(
            transaction_id=transaction.transaction_id,
            card_number="8600490744313347",
            expiry="2410"
        )
        print("Transaction pre-confirmed successfully")

        # Step 3: Confirm the transaction
        print("\nStep 3: Confirming the transaction")
        result = client.confirm_transaction(
            transaction_id=transaction.transaction_id,
            otp="111111"
        )
        print("Transaction confirmed successfully")
        print(f"Transaction ID: {result.store_transaction.trans_id}")
        print(f"Amount: {result.store_transaction.amount / 100:.2f}")
        print(f"Status: {result.store_transaction.status_message}")

        print("\n=== Payment flow completed successfully ===")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Run the tests
    print("=== Running mock tests ===\n")
    run_tests()

    # Simulate a payment flow
    simulate_payment_flow()
