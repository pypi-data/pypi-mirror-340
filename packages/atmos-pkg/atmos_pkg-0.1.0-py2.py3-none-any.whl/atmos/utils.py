"""
Utility functions for the Atmos API.
"""

import hashlib
from typing import Dict, Any


def validate_callback_signature(
    data: Dict[str, Any],
    api_key: str
) -> bool:
    """
    Validate the signature of a callback from Atmos.

    Args:
        data: The callback data
        api_key: The API key provided by Atmos

    Returns:
        True if the signature is valid
    """
    required_keys = ["store_id", "transaction_id", "invoice", "amount", "sign"]
    if not all(k in data for k in required_keys):
        return False

    # Extract the signature from the data
    received_sign = data["sign"]

    # Calculate the expected signature
    sign_parts = [
        data['store_id'],
        data['transaction_id'],
        data['invoice'],
        data['amount'],
        api_key
    ]
    sign_string = "".join(sign_parts)
    calculated_sign = hashlib.md5(sign_string.encode()).hexdigest()

    return received_sign == calculated_sign


def create_callback_response(
    success: bool, message: str = ""
) -> Dict[str, Any]:
    """
    Create a response for an Atmos callback.

    Args:
        success: Whether the callback was successful
        message: A message to include in the response

    Returns:
        A dictionary with the response data
    """
    return {
        "status": 1 if success else 0,
        "message": message or ("Успешно" if success else "Ошибка")
    }
