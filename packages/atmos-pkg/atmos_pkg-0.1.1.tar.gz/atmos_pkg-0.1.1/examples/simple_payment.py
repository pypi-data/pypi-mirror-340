"""
Example of a simple payment using the Atmos API.
"""

import os
import sys
import time

# Add the parent directory to the path so we can import the atmos package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from atmos import AtmosClient, AtmosAPIError


def main():
    # Initialize the client with your credentials
    # In a real application, you would get these from environment variables or a config file
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
            terminal_id="your_terminal_id"  # Optional if you have only one terminal
        )
        
        transaction_id = transaction.transaction_id
        print(f"Transaction created with ID: {transaction_id}")
        
        # Pre-confirm the transaction with a test card
        print("Pre-confirming transaction...")
        client.pre_confirm_transaction(
            transaction_id=transaction_id,
            card_number="8600490744313347",  # Test card
            expiry="2410"  # YYmm format
        )
        
        # In a real application, the user would receive an SMS with the OTP
        # For test cards, the OTP is always 111111
        print("Confirming transaction...")
        result = client.confirm_transaction(
            transaction_id=transaction_id,
            otp="111111"
        )
        
        # Check if the transaction was successful
        if result.store_transaction and result.store_transaction.confirmed:
            print(f"Transaction {transaction_id} was successful!")
            print(f"Amount: {result.store_transaction.amount / 100:.2f}")
            print(f"Card token: {result.store_transaction.card_id}")
        else:
            print("Transaction failed")
        
    except AtmosAPIError as e:
        print(f"API error: {e.code} - {e.message}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
