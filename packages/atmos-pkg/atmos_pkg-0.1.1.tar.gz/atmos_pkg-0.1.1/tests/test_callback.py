"""
Tests for the Atmos callback utilities.
"""

import unittest
import hashlib

from atmos.utils import validate_callback_signature, create_callback_response


class TestCallback(unittest.TestCase):
    """Tests for the callback utilities."""
    
    def setUp(self):
        """Set up the test case."""
        # Test API key
        self.api_key = "test_api_key"
        
        # Test callback data
        self.data = {
            "store_id": "test_store",
            "transaction_id": "123456",
            "invoice": "12345",
            "amount": "5000000"
        }
        
        # Generate a valid signature
        sign_string = f"{self.data['store_id']}{self.data['transaction_id']}{self.data['invoice']}{self.data['amount']}{self.api_key}"
        self.valid_signature = hashlib.md5(sign_string.encode()).hexdigest()
    
    def test_validate_callback_signature_valid(self):
        """Test validating a valid callback signature."""
        # Add the valid signature to the data
        data = self.data.copy()
        data["sign"] = self.valid_signature
        
        # Validate the signature
        result = validate_callback_signature(data, self.api_key)
        
        # Check the result
        self.assertTrue(result)
    
    def test_validate_callback_signature_invalid(self):
        """Test validating an invalid callback signature."""
        # Add an invalid signature to the data
        data = self.data.copy()
        data["sign"] = "invalid_signature"
        
        # Validate the signature
        result = validate_callback_signature(data, self.api_key)
        
        # Check the result
        self.assertFalse(result)
    
    def test_validate_callback_signature_missing_fields(self):
        """Test validating a callback signature with missing fields."""
        # Create data with missing fields
        for field in ["store_id", "transaction_id", "invoice", "amount"]:
            data = self.data.copy()
            del data[field]
            data["sign"] = self.valid_signature
            
            # Validate the signature
            result = validate_callback_signature(data, self.api_key)
            
            # Check the result
            self.assertFalse(result)
    
    def test_create_callback_response_success(self):
        """Test creating a success callback response."""
        # Create a success response
        response = create_callback_response(True)
        
        # Check the response
        self.assertEqual(response["status"], 1)
        self.assertEqual(response["message"], "Успешно")
        
        # Create a success response with a custom message
        response = create_callback_response(True, "Payment successful")
        
        # Check the response
        self.assertEqual(response["status"], 1)
        self.assertEqual(response["message"], "Payment successful")
    
    def test_create_callback_response_error(self):
        """Test creating an error callback response."""
        # Create an error response
        response = create_callback_response(False)
        
        # Check the response
        self.assertEqual(response["status"], 0)
        self.assertEqual(response["message"], "Ошибка")
        
        # Create an error response with a custom message
        response = create_callback_response(False, "Invalid signature")
        
        # Check the response
        self.assertEqual(response["status"], 0)
        self.assertEqual(response["message"], "Invalid signature")


if __name__ == "__main__":
    unittest.main()
