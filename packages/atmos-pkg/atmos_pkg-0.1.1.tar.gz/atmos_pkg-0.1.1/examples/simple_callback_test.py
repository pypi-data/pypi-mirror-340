"""
Simple test for the Atmos callback utilities.
"""

import os
import sys
import hashlib

# Add the parent directory to the path so we can import the atmos package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from atmos.utils import validate_callback_signature, create_callback_response


def test_callback_validation():
    """Test the callback validation functionality."""
    # Test API key
    api_key = "test_api_key"
    
    # Test callback data
    data = {
        "store_id": "test_store",
        "transaction_id": "123456",
        "invoice": "12345",
        "amount": "5000000"
    }
    
    # Generate a valid signature
    sign_string = f"{data['store_id']}{data['transaction_id']}{data['invoice']}{data['amount']}{api_key}"
    valid_signature = hashlib.md5(sign_string.encode()).hexdigest()
    
    # Test with a valid signature
    data_with_valid_signature = data.copy()
    data_with_valid_signature["sign"] = valid_signature
    
    result = validate_callback_signature(data_with_valid_signature, api_key)
    print(f"Valid signature test: {'PASSED' if result else 'FAILED'}")
    
    # Test with an invalid signature
    data_with_invalid_signature = data.copy()
    data_with_invalid_signature["sign"] = "invalid_signature"
    
    result = validate_callback_signature(data_with_invalid_signature, api_key)
    print(f"Invalid signature test: {'PASSED' if not result else 'FAILED'}")
    
    # Test with missing fields
    for field in ["store_id", "transaction_id", "invoice", "amount"]:
        data_with_missing_field = data.copy()
        del data_with_missing_field[field]
        data_with_missing_field["sign"] = valid_signature
        
        result = validate_callback_signature(data_with_missing_field, api_key)
        print(f"Missing {field} test: {'PASSED' if not result else 'FAILED'}")


def test_callback_response():
    """Test the callback response functionality."""
    # Test success response
    success_response = create_callback_response(True)
    print(f"Success response: {success_response}")
    print(f"Success response test: {'PASSED' if success_response['status'] == 1 else 'FAILED'}")
    
    # Test success response with custom message
    success_response_with_message = create_callback_response(True, "Payment successful")
    print(f"Success response with message: {success_response_with_message}")
    print(f"Success response with message test: {'PASSED' if success_response_with_message['message'] == 'Payment successful' else 'FAILED'}")
    
    # Test error response
    error_response = create_callback_response(False)
    print(f"Error response: {error_response}")
    print(f"Error response test: {'PASSED' if error_response['status'] == 0 else 'FAILED'}")
    
    # Test error response with custom message
    error_response_with_message = create_callback_response(False, "Invalid signature")
    print(f"Error response with message: {error_response_with_message}")
    print(f"Error response with message test: {'PASSED' if error_response_with_message['message'] == 'Invalid signature' else 'FAILED'}")


def main():
    """Run the tests."""
    print("\n=== Testing Atmos Callback Validation ===\n")
    test_callback_validation()
    
    print("\n=== Testing Atmos Callback Response ===\n")
    test_callback_response()
    
    print("\n=== All tests completed! ===")


if __name__ == "__main__":
    main()
