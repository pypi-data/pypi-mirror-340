"""
Atmos API Client

This module provides the main client for interacting with the Atmos payment
API.
"""

import base64
import time
from typing import Dict, List, Optional

import requests

from .exceptions import AtmosAPIError, AtmosAuthError
from .models import Transaction, TransactionResponse, Card, OfdItem


class AtmosClient:
    """
    Client for the Atmos payment API.

    This client handles authentication and provides methods for interacting
    with the Atmos payment API.
    """

    PRODUCTION_BASE_URL = "https://partner.atmos.uz"
    # Assuming there's a test URL
    TEST_BASE_URL = "https://test-partner.atmos.uz"

    # pylint: disable=too-many-arguments
    # These arguments are required for the Atmos API
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        store_id: str,
        test_mode: bool = False,
        language: str = "en"
    ):
        """
        Initialize the Atmos API client.

        Args:
            consumer_key: The consumer key provided by Atmos
            consumer_secret: The consumer secret provided by Atmos
            store_id: The store ID provided by Atmos
            test_mode: Whether to use the test environment
            language: The language for API responses (en, ru, uz)
        """
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.store_id = store_id
        # Set the base URL based on test mode
        if test_mode:
            self.base_url = self.TEST_BASE_URL
        else:
            self.base_url = self.PRODUCTION_BASE_URL
        self.language = language
        self.access_token = None
        self.token_expires_at = 0

    def _get_auth_header(self) -> str:
        """
        Get the Basic Auth header for token requests.

        Returns:
            The Basic Auth header value
        """
        auth_string = f"{self.consumer_key}:{self.consumer_secret}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        return f"Basic {encoded_auth}"

    def _get_token(self) -> str:
        """
        Get an access token from the Atmos API.

        Returns:
            The access token

        Raises:
            AtmosAuthError: If authentication fails
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": self._get_auth_header()
        }

        data = {
            "grant_type": "client_credentials"
        }

        response = requests.post(
            f"{self.base_url}/token",
            headers=headers,
            data=data,
            timeout=30  # Add timeout to prevent hanging
        )

        if response.status_code != 200:
            raise AtmosAuthError(f"Authentication failed: {response.text}")

        token_data = response.json()
        self.access_token = token_data["access_token"]
        # Set token expiry time (with a small buffer)
        self.token_expires_at = time.time() + token_data["expires_in"] - 60

        return self.access_token

    def _ensure_token(self) -> str:
        """
        Ensure we have a valid access token.

        Returns:
            The access token
        """
        if not self.access_token or time.time() > self.token_expires_at:
            return self._get_token()
        return self.access_token

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        params: Optional[Dict] = None
    ) -> Dict:
        """
        Make a request to the Atmos API.

        Args:
            method: The HTTP method to use
            endpoint: The API endpoint to call
            data: The request data
            params: The query parameters

        Returns:
            The response data

        Raises:
            AtmosAPIError: If the API returns an error
        """
        token = self._ensure_token()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        url = f"{self.base_url}{endpoint}"

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            params=params,
            timeout=30  # Add timeout to prevent hanging
        )

        response_data = response.json()

        # Check for API errors
        has_result = "result" in response_data
        result_ok = has_result and response_data["result"]["code"] == "OK"
        if not result_ok:
            raise AtmosAPIError(
                code=response_data["result"]["code"],
                message=response_data["result"]["description"]
            )

        return response_data

    def create_transaction(
        self,
        amount: int,
        account: str,
        terminal_id: Optional[str] = None,
        details: Optional[str] = None
    ) -> TransactionResponse:
        """
        Create a new transaction.

        Args:
            amount: The transaction amount in tiyins
            account: The payment identifier
            terminal_id: The terminal ID (optional if only one terminal is
                registered)
            details: Additional transaction details

        Returns:
            The transaction response
        """
        data = {
            "amount": amount,
            "account": account,
            "store_id": self.store_id,
            "lang": self.language
        }

        if terminal_id:
            data["terminal_id"] = terminal_id

        if details:
            data["details"] = details

        response = self._request("POST", "/merchant/pay/create", data)

        return TransactionResponse.from_dict(response)

    # pylint: disable=too-many-arguments
    # These arguments are required for the Atmos API OFD transaction
    def create_ofd_transaction(
        self,
        amount: int,
        account: str,
        ofd_items: List[OfdItem],
        terminal_id: Optional[str] = None,
        details: Optional[str] = None
    ) -> TransactionResponse:
        """
        Create a new OFD transaction with fiscal items.

        Args:
            amount: The transaction amount in tiyins
            account: The payment identifier
            ofd_items: List of OFD items
            terminal_id: The terminal ID (optional if only one terminal is
                registered)
            details: Additional transaction details

        Returns:
            The transaction response
        """
        data = {
            "amount": amount,
            "account": account,
            "store_id": self.store_id,
            "lang": self.language,
            "ofd_items": [item.to_dict() for item in ofd_items]
        }

        if terminal_id:
            data["terminal_id"] = terminal_id

        if details:
            data["details"] = details

        endpoint = "/merchant/pay/create/checkout-ofd"
        response = self._request("POST", endpoint, data)

        return TransactionResponse.from_dict(response)

    def pre_confirm_transaction(
        self,
        transaction_id: int,
        card_token: Optional[str] = None,
        card_number: Optional[str] = None,
        expiry: Optional[str] = None
    ) -> bool:
        """
        Pre-confirm a transaction.

        Args:
            transaction_id: The transaction ID
            card_token: The card token (for saved cards)
            card_number: The card number (for new cards)
            expiry: The card expiry date in format YYmm (for new cards)

        Returns:
            True if pre-confirmation was successful

        Note:
            Either card_token OR (card_number AND expiry) must be provided
        """
        if not card_token and not (card_number and expiry):
            raise ValueError(
                "Either card_token OR (card_number AND expiry) "
                "must be provided"
            )

        if card_token and (card_number or expiry):
            raise ValueError(
                "Cannot provide both card_token and card_number/expiry"
            )

        data = {
            "transaction_id": transaction_id,
            "store_id": self.store_id
        }

        if card_token:
            data["card_token"] = card_token
        else:
            data["card_number"] = card_number
            data["expiry"] = expiry

        response = self._request("POST", "/merchant/pay/pre-apply", data)

        return response["result"]["code"] == "OK"

    def confirm_transaction(
        self,
        transaction_id: int,
        otp: str
    ) -> TransactionResponse:
        """
        Confirm a transaction.

        Args:
            transaction_id: The transaction ID
            otp: The one-time password (SMS code or 111111 for token payments)

        Returns:
            The transaction response
        """
        data = {
            "transaction_id": transaction_id,
            "otp": otp,
            "store_id": self.store_id
        }

        response = self._request("POST", "/merchant/pay/apply", data)

        return TransactionResponse.from_dict(response)

    def create_multi_transaction(
        self,
        transactions: List[Transaction]
    ) -> TransactionResponse:
        """
        Create multiple transactions in a single request.

        Args:
            transactions: List of transactions to create

        Returns:
            The transaction response
        """
        data = {
            "store_id": self.store_id,
            "params": [t.to_dict() for t in transactions]
        }

        response = self._request("POST", "/merchant/bulk/pay/create", data)

        return TransactionResponse.from_dict(response)

    def pre_confirm_multi_transaction(
        self,
        transaction_ids: List[int],
        card_token: Optional[str] = None,
        card_number: Optional[str] = None,
        expiry: Optional[str] = None
    ) -> bool:
        """
        Pre-confirm multiple transactions.

        Args:
            transaction_ids: List of transaction IDs
            card_token: The card token (for saved cards)
            card_number: The card number (for new cards)
            expiry: The card expiry date in format YYmm (for new cards)

        Returns:
            True if pre-confirmation was successful

        Note:
            Either card_token OR (card_number AND expiry) must be provided
        """
        if not card_token and not (card_number and expiry):
            raise ValueError(
                "Either card_token OR (card_number AND expiry) "
                "must be provided"
            )

        if card_token and (card_number or expiry):
            raise ValueError(
                "Cannot provide both card_token and card_number/expiry"
            )

        data = {
            "transaction_id": transaction_ids,
            "store_id": self.store_id
        }

        if card_token:
            data["card_token"] = card_token
        else:
            data["card_number"] = card_number
            data["expiry"] = expiry

        response = self._request("POST", "/merchant/bulk/pay/pre-apply", data)

        return response["result"]["code"] == "OK"

    def confirm_multi_transaction(
        self,
        transaction_ids: List[int],
        otp: str
    ) -> TransactionResponse:
        """
        Confirm multiple transactions.

        Args:
            transaction_ids: List of transaction IDs
            otp: The one-time password (SMS code or 111111 for token payments)

        Returns:
            The transaction response
        """
        data = {
            "transaction_id": transaction_ids,
            "otp": otp,
            "store_id": self.store_id
        }

        response = self._request("POST", "/merchant/bulk/pay/apply", data)

        return TransactionResponse.from_dict(response)

    def confirm_ofd_transaction(
        self,
        transaction_id: int,
        otp: str,
        ofd_items: List[OfdItem]
    ) -> TransactionResponse:
        """
        Confirm a transaction with OFD items.

        Args:
            transaction_id: The transaction ID
            otp: The one-time password (SMS code or 111111 for token payments)
            ofd_items: List of OFD items

        Returns:
            The transaction response
        """
        data = {
            "transaction_id": transaction_id,
            "otp": otp,
            "store_id": self.store_id,
            "ofd_items": [item.to_dict() for item in ofd_items]
        }

        endpoint = "/merchant/pay/confirm-with-ofd-list"
        response = self._request("POST", endpoint, data)

        return TransactionResponse.from_dict(response)

    def get_transaction_info(self, transaction_id: int) -> Dict:
        """
        Get information about a transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The transaction information
        """
        data = {
            "transaction_id": transaction_id,
            "store_id": self.store_id
        }

        response = self._request("POST", "/merchant/pay/info", data)

        return response

    def cancel_transaction(self, transaction_id: int) -> bool:
        """
        Cancel a transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            True if cancellation was successful
        """
        data = {
            "transaction_id": transaction_id,
            "store_id": self.store_id
        }

        response = self._request("POST", "/merchant/pay/cancel", data)

        return response["result"]["code"] == "OK"

    def request_card_binding(
        self,
        card_number: str,
        expiry: str,
        phone: str
    ) -> Dict:
        """
        Request to bind a card to the merchant.

        Args:
            card_number: The card number
            expiry: The card expiry date in format YYmm
            phone: The phone number associated with the card

        Returns:
            The binding request response
        """
        data = {
            "card_number": card_number,
            "expiry": expiry,
            "phone": phone,
            "store_id": self.store_id
        }

        response = self._request("POST", "/merchant/card/bind", data)

        return response

    def confirm_card_binding(
        self,
        binding_id: int,
        otp: str
    ) -> Dict:
        """
        Confirm a card binding.

        Args:
            binding_id: The binding request ID
            otp: The one-time password (SMS code)

        Returns:
            The binding confirmation response
        """
        data = {
            "binding_id": binding_id,
            "otp": otp,
            "store_id": self.store_id
        }

        response = self._request("POST", "/merchant/card/bind/confirm", data)

        return response

    def get_bound_cards(self) -> List[Card]:
        """
        Get a list of cards bound to the merchant.

        Returns:
            List of bound cards
        """
        data = {
            "store_id": self.store_id
        }

        response = self._request("POST", "/merchant/card/list", data)

        cards = []
        for card_data in response.get("cards", []):
            cards.append(Card.from_dict(card_data))

        return cards

    def unbind_card(self, card_token: str) -> bool:
        """
        Unbind a card from the merchant.

        Args:
            card_token: The card token

        Returns:
            True if unbinding was successful
        """
        data = {
            "card_token": card_token,
            "store_id": self.store_id
        }

        response = self._request("POST", "/merchant/card/unbind", data)

        return response["result"]["code"] == "OK"

    def get_payment_page_url(
        self,
        transaction_id: int,
        redirect_url: Optional[str] = None
    ) -> str:
        """
        Get the URL for the payment page.

        Args:
            transaction_id: The transaction ID
            redirect_url: The URL to redirect to after payment

        Returns:
            The payment page URL
        """
        base = "https://checkout.pays.uz/invoice/get"
        url = f"{base}?storeId={self.store_id}&transactionId={transaction_id}"

        if redirect_url:
            url += f"&redirectLink={redirect_url}"

        return url

    def get_test_payment_page_url(
        self,
        transaction_id: int,
        redirect_url: Optional[str] = None
    ) -> str:
        """
        Get the URL for the test payment page.

        Args:
            transaction_id: The transaction ID
            redirect_url: The URL to redirect to after payment

        Returns:
            The test payment page URL
        """
        base = "http://test-checkout.pays.uz/invoice/get"
        url = f"{base}?storeId={self.store_id}&transactionId={transaction_id}"

        if redirect_url:
            url += f"&redirectLink={redirect_url}"

        return url
