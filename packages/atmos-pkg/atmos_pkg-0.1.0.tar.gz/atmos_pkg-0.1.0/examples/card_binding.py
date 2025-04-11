"""
Example of card binding and payment with a bound card using the Atmos API.
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
        # Request to bind a card
        print("Requesting card binding...")
        binding = client.request_card_binding(
            card_number="8600490744313347",  # Test card
            expiry="2410",  # YYmm format
            phone="+998901234567"  # Phone number associated with the card
        )
        
        binding_id = binding["binding_id"]
        print(f"Binding request created with ID: {binding_id}")
        
        # In a real application, the user would receive an SMS with the OTP
        # For test cards, the OTP is always 111111
        print("Confirming card binding...")
        result = client.confirm_card_binding(
            binding_id=binding_id,
            otp="111111"
        )
        
        # Get the card token from the result
        card_token = result["card_token"]
        print(f"Card bound successfully with token: {card_token}")
        
        # Create a transaction
        print("Creating transaction...")
        transaction = client.create_transaction(
            amount=5000000,  # 50,000.00 currency units
            account="12345"  # Your internal payment identifier
        )
        
        transaction_id = transaction.transaction_id
        print(f"Transaction created with ID: {transaction_id}")
        
        # Pre-confirm the transaction with the bound card
        print("Pre-confirming transaction with bound card...")
        client.pre_confirm_transaction(
            transaction_id=transaction_id,
            card_token=card_token
        )
        
        # For token payments, the OTP is always 111111
        print("Confirming transaction...")
        result = client.confirm_transaction(
            transaction_id=transaction_id,
            otp="111111"
        )
        
        # Check if the transaction was successful
        if result.store_transaction and result.store_transaction.confirmed:
            print(f"Transaction {transaction_id} was successful!")
            print(f"Amount: {result.store_transaction.amount / 100:.2f}")
        else:
            print("Transaction failed")
        
        # Get all bound cards
        print("Getting bound cards...")
        cards = client.get_bound_cards()
        print(f"Found {len(cards)} bound cards:")
        for card in cards:
            print(f"Card: {card.masked_pan}, Token: {card.token}")
        
    except AtmosAPIError as e:
        print(f"API error: {e.code} - {e.message}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
