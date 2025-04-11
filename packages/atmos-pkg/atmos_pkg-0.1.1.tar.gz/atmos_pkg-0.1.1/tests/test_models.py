"""
Tests for the Atmos API models.
"""

import unittest

from atmos.models import OfdItem, Card, Transaction, StoreTransaction, TransactionResponse


class TestModels(unittest.TestCase):
    """Tests for the model classes."""
    
    def test_ofd_item(self):
        """Test the OfdItem class."""
        # Create an OfdItem
        item = OfdItem(
            ofd_code="123456789",
            name="Test Product",
            amount=5000,
            quantity=2
        )
        
        # Check the attributes
        self.assertEqual(item.ofd_code, "123456789")
        self.assertEqual(item.name, "Test Product")
        self.assertEqual(item.amount, 5000)
        self.assertEqual(item.quantity, 2)
        
        # Check the to_dict method
        item_dict = item.to_dict()
        self.assertEqual(item_dict["ofd_code"], "123456789")
        self.assertEqual(item_dict["name"], "Test Product")
        self.assertEqual(item_dict["amount"], 5000)
        self.assertEqual(item_dict["quantity"], 2)
        
        # Check the from_dict method
        item2 = OfdItem.from_dict({
            "ofd_code": "987654321",
            "name": "Another Product",
            "amount": 10000,
            "quantity": 3
        })
        self.assertEqual(item2.ofd_code, "987654321")
        self.assertEqual(item2.name, "Another Product")
        self.assertEqual(item2.amount, 10000)
        self.assertEqual(item2.quantity, 3)
        
        # Check the from_dict method with ofdCode
        item3 = OfdItem.from_dict({
            "ofdCode": "111111111",
            "name": "Third Product",
            "amount": 15000
        })
        self.assertEqual(item3.ofd_code, "111111111")
        self.assertEqual(item3.name, "Third Product")
        self.assertEqual(item3.amount, 15000)
        self.assertEqual(item3.quantity, 1)  # Default value
    
    def test_card(self):
        """Test the Card class."""
        # Create a Card
        card = Card(
            token="test_token",
            masked_pan="860049******3347",
            expiry="2410",
            card_type="UZCARD",
            status=True
        )
        
        # Check the attributes
        self.assertEqual(card.token, "test_token")
        self.assertEqual(card.masked_pan, "860049******3347")
        self.assertEqual(card.expiry, "2410")
        self.assertEqual(card.card_type, "UZCARD")
        self.assertTrue(card.status)
        
        # Check the to_dict method
        card_dict = card.to_dict()
        self.assertEqual(card_dict["token"], "test_token")
        self.assertEqual(card_dict["masked_pan"], "860049******3347")
        self.assertEqual(card_dict["expiry"], "2410")
        self.assertEqual(card_dict["card_type"], "UZCARD")
        self.assertTrue(card_dict["status"])
        
        # Check the from_dict method
        card2 = Card.from_dict({
            "token": "another_token",
            "masked_pan": "986009******1907",
            "expiry": "2505",
            "card_type": "HUMO",
            "status": False
        })
        self.assertEqual(card2.token, "another_token")
        self.assertEqual(card2.masked_pan, "986009******1907")
        self.assertEqual(card2.expiry, "2505")
        self.assertEqual(card2.card_type, "HUMO")
        self.assertFalse(card2.status)
        
        # Check the from_dict method with card_id and card_number
        card3 = Card.from_dict({
            "card_id": "third_token",
            "card_number": "860031******4318"
        })
        self.assertEqual(card3.token, "third_token")
        self.assertEqual(card3.masked_pan, "860031******4318")
        self.assertIsNone(card3.expiry)
        self.assertIsNone(card3.card_type)
        self.assertTrue(card3.status)  # Default value
    
    def test_transaction(self):
        """Test the Transaction class."""
        # Create a Transaction
        transaction = Transaction(
            account="12345",
            amount=5000000,
            terminal_id="test_terminal",
            details="Test payment"
        )
        
        # Check the attributes
        self.assertEqual(transaction.account, "12345")
        self.assertEqual(transaction.amount, 5000000)
        self.assertEqual(transaction.terminal_id, "test_terminal")
        self.assertEqual(transaction.details, "Test payment")
        
        # Check the to_dict method
        transaction_dict = transaction.to_dict()
        self.assertEqual(transaction_dict["account"], "12345")
        self.assertEqual(transaction_dict["amount"], 5000000)
        self.assertEqual(transaction_dict["terminal_id"], "test_terminal")
        self.assertEqual(transaction_dict["details"], "Test payment")
        
        # Create a Transaction without optional fields
        transaction2 = Transaction(
            account="67890",
            amount=1000000
        )
        
        # Check the attributes
        self.assertEqual(transaction2.account, "67890")
        self.assertEqual(transaction2.amount, 1000000)
        self.assertIsNone(transaction2.terminal_id)
        self.assertIsNone(transaction2.details)
        
        # Check the to_dict method
        transaction_dict2 = transaction2.to_dict()
        self.assertEqual(transaction_dict2["account"], "67890")
        self.assertEqual(transaction_dict2["amount"], 1000000)
        self.assertNotIn("terminal_id", transaction_dict2)
        self.assertNotIn("details", transaction_dict2)
    
    def test_store_transaction(self):
        """Test the StoreTransaction class."""
        # Create a StoreTransaction
        transaction = StoreTransaction(
            trans_id=123456,
            account="12345",
            amount=5000000,
            terminal_id="test_terminal",
            confirmed=True,
            total=5000000,
            success_trans_id=654321,
            prepay_time=1635828973000,
            confirm_time=1635829043427,
            details="Test payment",
            card_id="test_token",
            status_code="0",
            status_message="Success",
            ofd_url="https://ofd.atmos.uz/api/ofd/123456"
        )
        
        # Check the attributes
        self.assertEqual(transaction.trans_id, 123456)
        self.assertEqual(transaction.account, "12345")
        self.assertEqual(transaction.amount, 5000000)
        self.assertEqual(transaction.terminal_id, "test_terminal")
        self.assertTrue(transaction.confirmed)
        self.assertEqual(transaction.total, 5000000)
        self.assertEqual(transaction.success_trans_id, 654321)
        self.assertEqual(transaction.prepay_time, 1635828973000)
        self.assertEqual(transaction.confirm_time, 1635829043427)
        self.assertEqual(transaction.details, "Test payment")
        self.assertEqual(transaction.card_id, "test_token")
        self.assertEqual(transaction.status_code, "0")
        self.assertEqual(transaction.status_message, "Success")
        self.assertEqual(transaction.ofd_url, "https://ofd.atmos.uz/api/ofd/123456")
        
        # Check the from_dict method
        transaction2 = StoreTransaction.from_dict({
            "trans_id": 789012,
            "account": "67890",
            "amount": 1000000,
            "terminal_id": "another_terminal",
            "confirmed": False,
            "total": 1000000
        })
        self.assertEqual(transaction2.trans_id, 789012)
        self.assertEqual(transaction2.account, "67890")
        self.assertEqual(transaction2.amount, 1000000)
        self.assertEqual(transaction2.terminal_id, "another_terminal")
        self.assertFalse(transaction2.confirmed)
        self.assertEqual(transaction2.total, 1000000)
        self.assertIsNone(transaction2.success_trans_id)
        self.assertIsNone(transaction2.prepay_time)
        self.assertIsNone(transaction2.confirm_time)
        self.assertIsNone(transaction2.details)
        self.assertIsNone(transaction2.card_id)
        self.assertIsNone(transaction2.status_code)
        self.assertIsNone(transaction2.status_message)
        self.assertIsNone(transaction2.ofd_url)
    
    def test_transaction_response(self):
        """Test the TransactionResponse class."""
        # Create a TransactionResponse with a single transaction
        response = TransactionResponse(
            result_code="OK",
            result_description="No errors",
            transaction_id=123456,
            store_transaction=StoreTransaction(
                trans_id=123456,
                account="12345",
                amount=5000000,
                terminal_id="test_terminal",
                confirmed=True,
                total=5000000
            )
        )
        
        # Check the attributes
        self.assertEqual(response.result_code, "OK")
        self.assertEqual(response.result_description, "No errors")
        self.assertEqual(response.transaction_id, 123456)
        self.assertEqual(response.store_transaction.trans_id, 123456)
        
        # Create a TransactionResponse with multiple transactions
        response2 = TransactionResponse(
            result_code="OK",
            result_description="No errors",
            transaction_id=[123456, 789012],
            store_transaction=[
                StoreTransaction(
                    trans_id=123456,
                    account="12345",
                    amount=5000000,
                    terminal_id="test_terminal",
                    confirmed=True,
                    total=5000000
                ),
                StoreTransaction(
                    trans_id=789012,
                    account="67890",
                    amount=1000000,
                    terminal_id="another_terminal",
                    confirmed=True,
                    total=1000000
                )
            ]
        )
        
        # Check the attributes
        self.assertEqual(response2.result_code, "OK")
        self.assertEqual(response2.result_description, "No errors")
        self.assertEqual(response2.transaction_id, [123456, 789012])
        self.assertEqual(len(response2.store_transaction), 2)
        self.assertEqual(response2.store_transaction[0].trans_id, 123456)
        self.assertEqual(response2.store_transaction[1].trans_id, 789012)
        
        # Check the from_dict method with a single transaction
        response3 = TransactionResponse.from_dict({
            "result": {
                "code": "OK",
                "description": "No errors"
            },
            "transaction_id": 123456,
            "store_transaction": {
                "trans_id": 123456,
                "account": "12345",
                "amount": 5000000,
                "terminal_id": "test_terminal",
                "confirmed": True,
                "total": 5000000
            }
        })
        self.assertEqual(response3.result_code, "OK")
        self.assertEqual(response3.result_description, "No errors")
        self.assertEqual(response3.transaction_id, 123456)
        self.assertEqual(response3.store_transaction.trans_id, 123456)
        
        # Check the from_dict method with multiple transactions
        response4 = TransactionResponse.from_dict({
            "result": {
                "code": "OK",
                "description": "No errors"
            },
            "transaction_id": [123456, 789012],
            "store_transaction": [
                {
                    "trans_id": 123456,
                    "account": "12345",
                    "amount": 5000000,
                    "terminal_id": "test_terminal",
                    "confirmed": True,
                    "total": 5000000
                },
                {
                    "trans_id": 789012,
                    "account": "67890",
                    "amount": 1000000,
                    "terminal_id": "another_terminal",
                    "confirmed": True,
                    "total": 1000000
                }
            ]
        })
        self.assertEqual(response4.result_code, "OK")
        self.assertEqual(response4.result_description, "No errors")
        self.assertEqual(response4.transaction_id, [123456, 789012])
        self.assertEqual(len(response4.store_transaction), 2)
        self.assertEqual(response4.store_transaction[0].trans_id, 123456)
        self.assertEqual(response4.store_transaction[1].trans_id, 789012)


if __name__ == '__main__':
    unittest.main()
