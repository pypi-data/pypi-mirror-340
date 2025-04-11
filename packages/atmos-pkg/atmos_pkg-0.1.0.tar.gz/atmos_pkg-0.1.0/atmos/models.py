"""
Data models for the Atmos API.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any, Union


@dataclass
class OfdItem:
    """
    Represents an OFD (fiscal) item.
    """
    ofd_code: str
    name: str
    amount: int
    quantity: int = 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        return {
            "ofd_code": self.ofd_code,
            "name": self.name,
            "amount": self.amount,
            "quantity": self.quantity
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OfdItem':
        """Create an OfdItem from a dictionary."""
        return cls(
            ofd_code=data.get("ofd_code") or data.get("ofdCode"),
            name=data.get("name", ""),
            amount=data.get("amount", 0),
            quantity=data.get("quantity", 1)
        )


@dataclass
class Card:
    """
    Represents a payment card.
    """
    token: str
    masked_pan: str
    expiry: Optional[str] = None
    card_type: Optional[str] = None
    status: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        result = {
            "token": self.token,
            "masked_pan": self.masked_pan,
            "status": self.status
        }

        if self.expiry:
            result["expiry"] = self.expiry

        if self.card_type:
            result["card_type"] = self.card_type

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Card':
        """Create a Card from a dictionary."""
        return cls(
            token=data.get("token") or data.get("card_id") or "",
            masked_pan=data.get("masked_pan") or data.get("card_number") or "",
            expiry=data.get("expiry"),
            card_type=data.get("card_type"),
            status=data.get("status", True)
        )


@dataclass
class Transaction:
    """
    Represents a transaction to be created.
    """
    account: str
    amount: int
    terminal_id: Optional[str] = None
    details: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        result = {
            "account": self.account,
            "amount": self.amount
        }

        if self.terminal_id:
            result["terminal_id"] = self.terminal_id

        if self.details:
            result["details"] = self.details

        return result


@dataclass
class StoreTransaction:
    """
    Represents a transaction returned by the API.
    """
    trans_id: int
    account: str
    amount: int
    terminal_id: str
    confirmed: bool
    total: int
    success_trans_id: Optional[int] = None
    prepay_time: Optional[int] = None
    confirm_time: Optional[int] = None
    details: Optional[str] = None
    card_id: Optional[str] = None
    status_code: Optional[str] = None
    status_message: Optional[str] = None
    ofd_url: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'StoreTransaction':
        """Create a StoreTransaction from a dictionary."""
        return cls(
            trans_id=data.get("trans_id", 0),
            account=data.get("account", ""),
            amount=data.get("amount", 0),
            terminal_id=data.get("terminal_id", ""),
            confirmed=data.get("confirmed", False),
            total=data.get("total", 0),
            success_trans_id=data.get("success_trans_id"),
            prepay_time=data.get("prepay_time"),
            confirm_time=data.get("confirm_time"),
            details=data.get("details"),
            card_id=data.get("card_id"),
            status_code=data.get("status_code"),
            status_message=data.get("status_message"),
            ofd_url=data.get("ofd_url")
        )


@dataclass
class TransactionResponse:
    """
    Represents a response from the API for transaction operations.
    """
    result_code: str
    result_description: str
    transaction_id: Optional[Union[int, List[int]]] = None
    # Store transaction can be a single transaction or a list of transactions
    store_transaction: Optional[
        Union[StoreTransaction, List[StoreTransaction]]
    ] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TransactionResponse':
        """Create a TransactionResponse from a dictionary."""
        result = data.get("result", {})

        # Handle single transaction
        store_transaction = None
        if "store_transaction" in data:
            if isinstance(data["store_transaction"], list):
                store_transaction = [
                    StoreTransaction.from_dict(t)
                    for t in data["store_transaction"]
                ]
            else:
                store_transaction = StoreTransaction.from_dict(
                    data["store_transaction"]
                )

        return cls(
            result_code=result.get("code", ""),
            result_description=result.get("description", ""),
            transaction_id=data.get("transaction_id"),
            store_transaction=store_transaction
        )
