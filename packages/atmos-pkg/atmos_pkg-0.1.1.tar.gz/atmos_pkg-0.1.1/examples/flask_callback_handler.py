"""
Example of a Flask application that handles Atmos callbacks.

This script demonstrates how to integrate the Atmos callback handler
with a Flask application.

To run this example:
1. Install Flask: pip install flask
2. Run the script: python flask_callback_handler.py
3. The server will listen on http://localhost:5000/atmos/callback
4. You can test it by sending a POST request to this endpoint with the
   expected data
"""

import os
import sys
import hashlib
import json
from flask import Flask, request, jsonify

# Add the parent directory to the path so we can import the atmos package
# Note: This import structure is common in example scripts but would be
# different in a real application where the package is properly installed
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# pylint: disable=wrong-import-position
from atmos.utils import validate_callback_signature, create_callback_response  # noqa

app = Flask(__name__)

# Your API key provided by Atmos
API_KEY = "test_api_key"

# In-memory database for storing payment information
payments_db = {}


@app.route('/atmos/callback', methods=['POST'])
def atmos_callback():
    """
    Handle callbacks from the Atmos API.

    Expected data:
    {
        "store_id": "your_store_id",
        "transaction_id": "123456",
        "transaction_time": "2023-01-01T12:00:00",
        "amount": "5000000",
        "invoice": "12345",
        "sign": "md5_hash_of_the_above_data_plus_api_key"
    }
    """
    data = request.json

    # Log the received data
    app.logger.info(f"Received callback data: {data}")

    # Validate the signature
    if not validate_callback_signature(data, API_KEY):
        app.logger.warning("Invalid signature")
        error_msg = "Invalid signature"
        return jsonify(create_callback_response(False, error_msg)), 400

    # Process the payment
    # Extract payment data (store_id is not used but kept for reference)
    # pylint: disable=unused-variable
    transaction_id = data["transaction_id"]
    transaction_time = data["transaction_time"]
    amount = data["amount"]
    invoice = data["invoice"]

    # Store the payment information
    payments_db[invoice] = {
        "transaction_id": transaction_id,
        "amount": int(amount) / 100,  # Convert to currency units
        "transaction_time": transaction_time,
        "status": "paid"
    }

    app.logger.info(f"Payment processed for invoice {invoice}")
    app.logger.info(f"Amount: {int(amount) / 100:.2f}")
    app.logger.info(f"Transaction ID: {transaction_id}")
    app.logger.info(f"Transaction time: {transaction_time}")

    # Return a success response
    success_msg = "Payment processed successfully"
    return jsonify(create_callback_response(True, success_msg))


@app.route('/payments/<invoice>', methods=['GET'])
def get_payment(invoice):
    """Get payment information for an invoice."""
    if invoice in payments_db:
        return jsonify(payments_db[invoice])
    return jsonify({"error": "Payment not found"}), 404


@app.route('/test-callback', methods=['GET'])
def test_callback():
    """Generate a test callback."""
    # Create test data
    data = {
        "store_id": "test_store",
        "transaction_id": "123456",
        "transaction_time": "2023-01-01T12:00:00",
        "amount": "5000000",
        "invoice": "12345"
    }

    # Generate a signature
    sign_parts = [
        data['store_id'],
        data['transaction_id'],
        data['invoice'],
        data['amount'],
        API_KEY
    ]
    sign_string = "".join(sign_parts)
    data["sign"] = hashlib.md5(sign_string.encode()).hexdigest()

    # Return the test data
    return jsonify({
        "callback_url": f"{request.host_url}atmos/callback",
        "test_data": data,
        "curl_command": (
            f"curl -X POST -H 'Content-Type: application/json' "
            f"-d '{json.dumps(data)}' {request.host_url}atmos/callback"
        )
    })


if __name__ == "__main__":
    app.run(debug=True)
    print("Server running on http://localhost:5000")
    print("Test the callback handler by visiting:")
    print("http://localhost:5000/test-callback")
