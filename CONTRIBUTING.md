# Contributing to VBaaS Python SDK

Thank you for your interest in contributing to the VBaaS Python SDK! This guide will help you get started.

## Development Setup

### Prerequisites
- Python 3.9 or higher
- Git

### Local Development
```bash
# Clone the repository
git clone https://github.com/GiddyNaya/vfd-vbaas.git
cd vbaas-python-sdk

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Check code quality
black --check .
isort --check-only .
flake8 vbaas/ tests/ examples/
mypy vbaas/
```

## Code Quality Standards

### Code Formatting
We use [Black](https://black.readthedocs.io/) for code formatting:
```bash
black .
```

### Import Sorting
We use [isort](https://pycqa.github.io/isort/) for import sorting:
```bash
isort .
```

### Linting
We use [flake8](https://flake8.pycqa.org/) for linting:
```bash
flake8 vbaas/ tests/ examples/
```

### Type Checking
We use [mypy](https://mypy.readthedocs.io/) for type checking:
```bash
mypy vbaas/
```

## Testing

### Running Tests
```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=vbaas --cov-report=html

# Run specific test file
pytest tests/test_client.py -v
```

### Writing Tests
- Tests should be in the `tests/` directory
- Use descriptive test names
- Mock external API calls
- Test both success and error scenarios

## Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes**
4. **Run quality checks**:
   ```bash
   black .
   isort .
   flake8 vbaas/ tests/ examples/
   mypy vbaas/
   pytest tests/ -v
   ```
5. **Commit your changes**: `git commit -m "Add feature description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**

## Release Process

### For Maintainers

1. **Update version**:
   ```bash
   python scripts/bump_version.py 1.0.1
   ```

2. **Commit and push**:
   ```bash
   git add pyproject.toml setup.py
   git commit -m "Bump version to 1.0.1"
   git push
   ```

3. **Create GitHub release** with tag `v1.0.1`

4. **GitHub Actions will automatically**:
   - Run tests on multiple Python versions
   - Check code quality
   - Build and publish to PyPI

## Project Structure

```
vbaas-python-sdk/
├── vbaas/                    # Main package
│   ├── __init__.py          # Package exports
│   ├── client.py            # Main client class
│   ├── models.py            # Data models
│   └── exceptions.py        # Custom exceptions
├── examples/                 # Usage examples
├── tests/                   # Test suite
├── scripts/                 # Development scripts
├── .github/workflows/       # CI/CD workflows
├── pyproject.toml          # Package configuration
└── README.md               # Documentation
```

## API Documentation

### VBaaSClient
The main client class for interacting with VBaaS APIs.

#### Methods
- `get_biller_categories()`: Get all available biller categories
- `get_billers(category_name)`: Get billers for a specific category
- `get_biller_items(biller_id, division_id, product_id)`: Get items for a biller
- `validate_customer(...)`: Validate customer information
- `pay_bill(...)`: Make a bill payment
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

## Questions or Issues?

- **Bug Reports**: Create an issue with detailed description
- **Feature Requests**: Create an issue with use case description
- **Questions**: Create an issue or reach out to maintainers

## Code of Conduct

Please be respectful and inclusive in all interactions. We welcome contributions from everyone regardless of background or experience level.

---

Thank you for contributing to VBaaS Python SDK! 🚀 