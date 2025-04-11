# Atmos Payment Provider Python Library

A Python library for integrating with the Atmos payment provider API.

## Installation

```bash
pip install atmos-pkg
```

## Features

- Authentication handling with automatic token refresh
- Payment processing (create, pre-apply, confirm transactions)
- Card binding functionality
- Transaction information retrieval
- Error handling
- Support for both single and multi-transactions
- Support for OFD (fiscal) transactions
- Callback validation utilities

## Usage

### Basic Usage

```python
from atmos import AtmosClient, OfdItem, Transaction

# Initialize the client
client = AtmosClient(
    consumer_key="your_consumer_key",
    consumer_secret="your_consumer_secret",
    store_id="your_store_id",
    test_mode=True  # Set to False for production
)

# Create a transaction
transaction = client.create_transaction(
    amount=5000000,  # Amount in tiyins (50,000.00 currency units)
    account="12345",  # Your internal payment identifier
    terminal_id="your_terminal_id"  # Optional if you have only one terminal
)

# Get the transaction ID
transaction_id = transaction.transaction_id

# Pre-confirm the transaction with a card
client.pre_confirm_transaction(
    transaction_id=transaction_id,
    card_number="8600490744313347",
    expiry="2410"  # YYmm format
)

# Confirm the transaction with the OTP code
# For test cards, the OTP is always 111111
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
```

### Creating an OFD Transaction

```python
# Create OFD items
ofd_items = [
    OfdItem(
        ofd_code="XXXXXXXXX",
        name="Product 1",
        amount=300000,  # 3,000.00 currency units
        quantity=1
    ),
    OfdItem(
        ofd_code="XXXXXXXXX",
        name="Product 2",
        amount=200000,  # 2,000.00 currency units
        quantity=2
    )
]

# Create an OFD transaction
transaction = client.create_ofd_transaction(
    amount=500000,  # Total amount in tiyins
    account="12345",
    ofd_items=ofd_items
)

# Pre-confirm and confirm as usual
# ...
```

### Creating Multiple Transactions

```python
# Create transaction objects
transactions = [
    Transaction(
        account="user_1",
        amount=50000,
        details="For service 1"
    ),
    Transaction(
        account="user_2",
        amount=100000,
        details="For service 2"
    )
]

# Create multiple transactions
result = client.create_multi_transaction(transactions)

# Get the transaction IDs
transaction_ids = result.transaction_id

# Pre-confirm the transactions
client.pre_confirm_multi_transaction(
    transaction_ids=transaction_ids,
    card_number="8600490744313347",
    expiry="2410"
)

# Confirm the transactions
result = client.confirm_multi_transaction(
    transaction_ids=transaction_ids,
    otp="111111"
)
```

### Card Binding

```python
# Request to bind a card
binding = client.request_card_binding(
    card_number="8600490744313347",
    expiry="2410",
    phone="+998901234567"
)

binding_id = binding["binding_id"]

# Confirm the binding with the OTP code
client.confirm_card_binding(
    binding_id=binding_id,
    otp="111111"
)

# Get bound cards
cards = client.get_bound_cards()
for card in cards:
    print(f"Card: {card.masked_pan}, Token: {card.token}")

# Use a bound card for payment
client.pre_confirm_transaction(
    transaction_id=transaction_id,
    card_token=cards[0].token
)

# For token payments, the OTP is always 111111
client.confirm_transaction(
    transaction_id=transaction_id,
    otp="111111"
)
```

### Handling Callbacks

```python
from atmos.utils import validate_callback_signature, create_callback_response
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/atmos/callback', methods=['POST'])
def atmos_callback():
    data = request.json

    # Validate the signature
    if not validate_callback_signature(data, api_key="your_api_key"):
        return jsonify(create_callback_response(False, "Invalid signature")), 400

    # Process the payment
    store_id = data["store_id"]
    transaction_id = data["transaction_id"]
    invoice = data["invoice"]
    amount = data["amount"]

    # Your payment processing logic here
    # ...

    # Return a success response
    return jsonify(create_callback_response(True, "Payment processed successfully"))
```

### Payment Page Integration

```python
# Create a transaction
transaction = client.create_transaction(
    amount=5000000,
    account="12345"
)

# Get the payment page URL
payment_url = client.get_payment_page_url(
    transaction_id=transaction.transaction_id,
    redirect_url="https://your-website.com/payment/success"
)

# Redirect the user to the payment page
# In a web framework like Flask:
# return redirect(payment_url)
```

## Error Handling

```python
from atmos import AtmosError, AtmosAPIError, AtmosAuthError

try:
    # Attempt to create a transaction
    transaction = client.create_transaction(
        amount=5000000,
        account="12345"
    )
except AtmosAuthError as e:
    print(f"Authentication error: {e}")
except AtmosAPIError as e:
    print(f"API error: {e.code} - {e.message}")
except AtmosError as e:
    print(f"General error: {e}")
```

## Testing

The library includes support for test mode, which uses the Atmos test environment. In test mode, you can use the test cards provided by Atmos:

- PAN: `8600490744313347` Expiry: `10/24`
- PAN: `8600332914249390` Expiry: `09/25`
- PAN: `8600492993407481` Expiry: `10/24`
- PAN: `8600312990314318` Expiry: `08/23`
- PAN: `9860090101431907` Expiry: `05/25`

For testing error scenarios:

- PAN: `8600312987000557` Expiry: `12/22` - Processing error
- PAN: `8600493214116133` Expiry: `10/24` - SMS not connected
- PAN: `8600492986215602` Expiry: `03/20` - Expired card
- PAN: `8600312998546358` Expiry: `10/23` - Insufficient funds

The OTP code for all test cards is `111111`.

## License

MIT
