"""
Simple mock test for the Atmos payment library.
"""

import os
import sys
# Add the parent directory to the path so we can import the atmos package
# Note: This import structure is common in example scripts but would be
# different in a real application where the package is properly installed
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# pylint: disable=wrong-import-position
from atmos import AtmosClient  # noqa


def mock_payment_flow():
    """Simulate a payment flow with mocks."""
    print("=== Simulating a payment flow with mocks ===\n")

    # Create a client
    client = AtmosClient(
        consumer_key="test_key",
        consumer_secret="test_secret",
        store_id="test_store",
        test_mode=True
    )

    # Mock the _request method
    # pylint: disable=protected-access
    # Note: In a mock implementation, it's acceptable to access
    # protected members
    original_request = client._request

    def mock_request(method, endpoint, data=None, params=None):
        """Mock the _request method."""
        print(f"Making {method} request to {endpoint}")
        print(f"Data: {data}")

        # In the real implementation, data is passed as json parameter
        # but for simplicity in this mock, we'll just use data

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

        if endpoint == "/merchant/pay/pre-apply":
            return {
                "result": {
                    "code": "OK",
                    "description": "No errors"
                }
            }

        if endpoint == "/merchant/pay/apply":
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
    # pylint: disable=protected-access
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

    except (ValueError, KeyError) as e:
        print(f"Data error: {e}")
    except ConnectionError as e:
        print(f"Connection error: {e}")


if __name__ == "__main__":
    mock_payment_flow()
