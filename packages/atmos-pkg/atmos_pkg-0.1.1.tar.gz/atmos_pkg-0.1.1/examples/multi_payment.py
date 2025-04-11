"""
Example of a multi-transaction payment using the Atmos API.
"""

import os
import sys
import time

# Add the parent directory to the path so we can import the atmos package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from atmos import AtmosClient, Transaction, AtmosAPIError


def main():
    # Initialize the client with your credentials
    client = AtmosClient(
        consumer_key="your_consumer_key",
        consumer_secret="your_consumer_secret",
        store_id="your_store_id",
        test_mode=True  # Use the test environment
    )
    
    try:
        # Create transaction objects
        transactions = [
            Transaction(
                account="user_1",
                amount=50000,  # 500.00 currency units
                details="For service 1"
            ),
            Transaction(
                account="user_2",
                amount=100000,  # 1,000.00 currency units
                details="For service 2"
            )
        ]
        
        # Create multiple transactions
        print("Creating multiple transactions...")
        result = client.create_multi_transaction(transactions)
        
        # Get the transaction IDs
        transaction_ids = result.transaction_id
        print(f"Transactions created with IDs: {transaction_ids}")
        
        # Pre-confirm the transactions with a test card
        print("Pre-confirming transactions...")
        client.pre_confirm_multi_transaction(
            transaction_ids=transaction_ids,
            card_number="8600490744313347",  # Test card
            expiry="2410"  # YYmm format
        )
        
        # Confirm the transactions
        print("Confirming transactions...")
        result = client.confirm_multi_transaction(
            transaction_ids=transaction_ids,
            otp="111111"  # For test cards, the OTP is always 111111
        )
        
        # Check if the transactions were successful
        if result.store_transaction and isinstance(result.store_transaction, list):
            print(f"All {len(result.store_transaction)} transactions were successful!")
            
            for i, transaction in enumerate(result.store_transaction):
                print(f"Transaction {i+1}:")
                print(f"  ID: {transaction.trans_id}")
                print(f"  Account: {transaction.account}")
                print(f"  Amount: {transaction.amount / 100:.2f}")
                print(f"  Status: {transaction.status_message}")
        else:
            print("Transactions failed")
        
    except AtmosAPIError as e:
        print(f"API error: {e.code} - {e.message}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
