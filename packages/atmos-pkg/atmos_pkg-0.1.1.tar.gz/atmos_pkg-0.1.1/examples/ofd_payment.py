"""
Example of an OFD payment using the Atmos API.
"""

import os
import sys
import time

# Add the parent directory to the path so we can import the atmos package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from atmos import AtmosClient, OfdItem, AtmosAPIError


def main():
    # Initialize the client with your credentials
    client = AtmosClient(
        consumer_key="your_consumer_key",
        consumer_secret="your_consumer_secret",
        store_id="your_store_id",
        test_mode=True  # Use the test environment
    )
    
    try:
        # Create OFD items
        ofd_items = [
            OfdItem(
                ofd_code="123456789",  # IKPU code of the product
                name="Product 1",
                amount=300000,  # 3,000.00 currency units
                quantity=1
            ),
            OfdItem(
                ofd_code="987654321",  # IKPU code of the product
                name="Product 2",
                amount=200000,  # 2,000.00 currency units
                quantity=2
            )
        ]
        
        # Create an OFD transaction
        print("Creating OFD transaction...")
        transaction = client.create_ofd_transaction(
            amount=500000,  # Total amount in tiyins
            account="12345",  # Your internal payment identifier
            ofd_items=ofd_items
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
        
        # Confirm the transaction with OFD items
        print("Confirming transaction with OFD items...")
        result = client.confirm_ofd_transaction(
            transaction_id=transaction_id,
            otp="111111",  # For test cards, the OTP is always 111111
            ofd_items=ofd_items
        )
        
        # Check if the transaction was successful
        if result.store_transaction and result.store_transaction.confirmed:
            print(f"Transaction {transaction_id} was successful!")
            print(f"Amount: {result.store_transaction.amount / 100:.2f}")
            
            # If there's a fiscal receipt URL, print it
            if result.store_transaction.ofd_url:
                print(f"Fiscal receipt URL: {result.store_transaction.ofd_url}")
        else:
            print("Transaction failed")
        
    except AtmosAPIError as e:
        print(f"API error: {e.code} - {e.message}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
