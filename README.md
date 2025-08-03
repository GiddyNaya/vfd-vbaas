# VFD VBaaS Python SDK

[![PyPI version](https://badge.fury.io/py/vbaas-python-sdk.svg)](https://badge.fury.io/py/vbaas-python-sdk)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/example/vbaas-python-sdk/workflows/Test/badge.svg)](https://github.com/example/vbaas-python-sdk/actions)
[![Lint](https://github.com/example/vbaas-python-sdk/workflows/Lint/badge.svg)](https://github.com/example/vbaas-python-sdk/actions)

An unofficial Python SDK for [VFD Bank as a Service (VBaaS) API](https://vbaas-docs.vfdtech.ng), providing easy integration with VBaaS services including bills payment functionality.

## Features

- **Authentication Management**: Automatic token generation and refresh
- **Bills Payment API**: Complete integration with VBaaS bills payment services
- **Environment Support**: Both test and live environment configurations
- **Type Safety**: Full type hints for better development experience
- **Error Handling**: Comprehensive error handling and response validation

## Installation

```bash
pip install vbaas-python-sdk
```

Or install from source:

```bash
git clone https://github.com/example/vbaas-python-sdk.git
cd vbaas-python-sdk
pip install -e .
```

## Quick Start

```python
from vbaas import VBaaSClient

# Initialize client
client = VBaaSClient(
    consumer_key="your_consumer_key",
    consumer_secret="your_consumer_secret",
    environment="test"  # or "live"
)

# Get biller categories
categories = client.get_biller_categories()
print(categories)

# Get billers for a category
billers = client.get_billers("Airtime")
print(billers)

# Make a bill payment
payment_result = client.pay_bill(
    customer_id="09071046909",
    amount="1000",
    division="C",
    payment_item="airtime",
    product_id="423",
    biller_id="airng",
    reference="your-unique-reference",
    phone_number="09000000000"
)
print(payment_result)

# Check transaction status
status = client.get_transaction_status("your-transaction-id")
print(status)
```

## API Reference

### VBaaSClient

The main client class for interacting with VBaaS APIs.

#### Methods

- `get_biller_categories()`: Get all available biller categories
- `get_billers(category_name)`: Get billers for a specific category
- `get_biller_items(biller_id, division_id, product_id)`: Get items for a biller
- `validate_customer(division_id, payment_item, customer_id, biller_id)`: Validate customer information
- `pay_bill(**kwargs)`: Make a bill payment
- `get_transaction_status(transaction_id)`: Check payment status

## Environment Configuration

The SDK supports both test and live environments:

- **Test Environment**: Use for development and testing
- **Live Environment**: Use for production

## Error Handling

The SDK provides comprehensive error handling:

```python
from vbaas import VBaaSClient, VBaaSError

try:
    client = VBaaSClient(consumer_key="key", consumer_secret="secret")
    result = client.pay_bill(...)
except VBaaSError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please contact [info@vfdtech.ng](mailto:info@vfdtech.ng) or visit the [documentation](https://vbaas-docs.vfdtech.ng).
