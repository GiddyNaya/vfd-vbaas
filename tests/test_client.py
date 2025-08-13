"""
Tests for VBaaS Client

Unit tests for the VBaaS Python SDK client using mock responses.
"""

from unittest.mock import Mock, patch

import pytest

from vbaas import VBaaSClient
from vbaas.exceptions import (
    APIError,
    ConfigurationError,
    ValidationError,
)


class TestVBaaSClient:
    """Test cases for VBaaSClient using mock responses."""

    def setup_method(self):
        """Set up test fixtures."""
        self.consumer_key = "test_consumer_key_12345"
        self.consumer_secret = "test_consumer_secret_67890"
        self.client = VBaaSClient(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            environment="test",
        )

    def teardown_method(self):
        """Clean up after each test."""
        if hasattr(self, "client"):
            self.client.close()

    def test_init_valid_config(self):
        """Test client initialization with valid configuration."""
        client = VBaaSClient(
            consumer_key="key", consumer_secret="secret", environment="test"
        )
        assert client.consumer_key == "key"
        assert client.consumer_secret == "secret"
        assert client.environment == "test"
        client.close()

    def test_init_invalid_environment(self):
        """Test client initialization with invalid environment."""
        with pytest.raises(ConfigurationError):
            VBaaSClient(
                consumer_key="key",
                consumer_secret="secret",
                environment="invalid",
            )

    def test_init_missing_credentials(self):
        """Test client initialization with missing credentials."""
        with pytest.raises(ConfigurationError):
            VBaaSClient(consumer_key="", consumer_secret="secret")

        with pytest.raises(ConfigurationError):
            VBaaSClient(consumer_key="key", consumer_secret="")

    @patch("requests.Session.post")
    def test_get_access_token_success(self, mock_post):
        """Test successful token retrieval."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "00",
            "message": "Successful",
            "data": {
                "access_token": "test_token",
                "scope": "am_application_scope default",
                "token_type": "Bearer",
                "expires_in": 9223372036854775807,
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        token = self.client._get_access_token()
        assert token == "test_token"
        assert self.client._access_token == "test_token"

    @patch.object(VBaaSClient, "_get_access_token")
    @patch("requests.Session.get")
    def test_get_biller_categories_success(self, mock_get, mock_token):
        """Test successful biller categories retrieval."""
        mock_token.return_value = "test_token"
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "00",
            "message": "Successfully Returned Biller Category",
            "data": [
                {"category": "Airtime"},
                {"category": "Cable TV"},
                {"category": "Data"},
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        categories = self.client.get_biller_categories()
        assert len(categories) == 3
        assert categories[0].category == "Airtime"
        assert categories[1].category == "Cable TV"
        assert categories[2].category == "Data"

    @patch.object(VBaaSClient, "_get_access_token")
    @patch("requests.Session.get")
    def test_get_billers_success(self, mock_get, mock_token):
        """Test successful billers retrieval."""
        mock_token.return_value = "test_token"
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "00",
            "message": "Successfully Returned Biller list",
            "data": [
                {
                    "id": "airng",
                    "name": "AIRTEL",
                    "division": "C",
                    "product": "423",
                    "category": "Airtime",
                }
            ],
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        billers = self.client.get_billers("Airtime")
        assert len(billers) == 1
        assert billers[0].id == "airng"
        assert billers[0].name == "AIRTEL"

    def test_get_billers_validation_error(self):
        """Test billers retrieval with invalid input."""
        with pytest.raises(ValidationError):
            self.client.get_billers("")

    @patch.object(VBaaSClient, "_get_access_token")
    @patch("requests.Session.get")
    def test_get_biller_items_success(self, mock_get, mock_token):
        """Test successful biller items retrieval."""
        mock_token.return_value = "test_token"
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "00",
            "message": "Successfully Returned Biller Items",
            "data": {
                "paymentitems": [
                    {
                        "id": "item1",
                        "billerid": "airng",
                        "amount": "1000",
                        "code": "CODE1",
                        "paymentitemname": "Airtime",
                        "productId": "423",
                        "paymentitemid": "pay1",
                        "currencySymbol": "₦",
                        "isAmountFixed": True,
                        "itemFee": "0",
                        "itemCurrencySymbol": "₦",
                        "pictureId": "pic1",
                        "paymentCode": "PAY1",
                        "sortOrder": "1",
                        "billerType": "type1",
                        "payDirectitemCode": "DIR1",
                        "currencyCode": "NGN",
                        "division": "C",
                        "categoryid": "cat1",
                        "createdDate": "2024-01-01",
                    }
                ]
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        items = self.client.get_biller_items(
            biller_id="airng", division_id="C", product_id="423"
        )
        assert len(items) == 1
        assert items[0].id == "item1"
        assert items[0].biller_id == "airng"

    def test_pay_bill_validation_error(self):
        """Test bill payment with missing parameters."""
        with pytest.raises(ValidationError):
            self.client.pay_bill(
                customer_id="",  # Missing customer_id
                amount="1000",
                division="C",
                payment_item="airtime",
                product_id="423",
                biller_id="airng",
                reference="test-ref-123",
                phone_number="08012345678",
            )

    @patch.object(VBaaSClient, "_get_access_token")
    @patch("requests.Session.get")
    def test_get_transaction_status_success(self, mock_get, mock_token):
        """Test successful transaction status retrieval."""
        mock_token.return_value = "test_token"
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "00",
            "message": "Successful Transaction Retrieval",
            "data": {
                "transactionStatus": "00",
                "amount": "1000",
                "token": "12345",
            },
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        status = self.client.get_transaction_status("test-transaction-id")
        assert status.status == "00"
        assert status.transaction_status == "00"
        assert status.amount == "1000"
        assert status.token == "12345"

    @patch.object(VBaaSClient, "_get_access_token")
    @patch("requests.Session.get")
    def test_get_transaction_status_not_found(self, mock_get, mock_token):
        """Test transaction status retrieval for non-existent transaction."""
        mock_token.return_value = "test_token"
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "108",
            "message": "No Transaction!",
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        status = self.client.get_transaction_status("non-existent-id")
        assert status.status == "108"
        assert status.message == "No Transaction!"

    def test_validate_response_success(self):
        """Test response validation with successful response."""
        response = {
            "status": "00",
            "message": "Success",
            "data": {"key": "value"},
        }

        validated = self.client._validate_response(response)
        assert validated == response

    def test_validate_response_failure(self):
        """Test response validation with failed response."""
        response = {"status": "99", "message": "Failed", "data": {}}

        with pytest.raises(APIError) as exc_info:
            self.client._validate_response(response)

        assert exc_info.value.message == "Failed"
        assert exc_info.value.status_code == "99"

    def test_close(self):
        """Test client cleanup."""
        # Create a new client for this test
        test_client = VBaaSClient(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            environment="test",
        )
        test_client.close()
        # If no exception is raised, the test passes
