"""
Tests for VBaaS Models

Unit tests for the VBaaS Python SDK models.
"""

from vbaas.models import (
    APIResponse,
    AuthToken,
    Biller,
    BillerCategory,
    BillerItem,
    PaymentRequest,
    PaymentResponse,
    TransactionStatus,
)


class TestModels:
    """Test cases for VBaaS models."""

    def test_biller_category(self):
        """Test BillerCategory model."""
        category = BillerCategory(category="Airtime")
        assert category.category == "Airtime"

    def test_biller(self):
        """Test Biller model."""
        biller = Biller(
            id="airng",
            name="AIRTEL",
            division="C",
            product="423",
            category="Airtime",
            convenience_fee="30",
        )
        assert biller.id == "airng"
        assert biller.name == "AIRTEL"
        assert biller.division == "C"
        assert biller.product == "423"
        assert biller.category == "Airtime"
        assert biller.convenience_fee == "30"

    def test_biller_without_convenience_fee(self):
        """Test Biller model without convenience fee."""
        biller = Biller(
            id="airng",
            name="AIRTEL",
            division="C",
            product="423",
            category="Airtime",
        )
        assert biller.convenience_fee is None

    def test_biller_item(self):
        """Test BillerItem model."""
        item = BillerItem(
            id="5",
            biller_id="airng",
            amount="0",
            code="2",
            payment_item_name="AIRNG",
            product_id="423",
            payment_item_id="423",
            currency_symbol="NGN",
            is_amount_fixed="false",
            item_fee="0",
            item_currency_symbol="NGN",
            picture_id="87",
            payment_code="airng",
            sort_order="4",
            biller_type="MO",
            pay_direct_item_code="airng",
            currency_code="566",
            division="C",
            category_id="3",
            created_date="2022-10-18 10:11:43",
        )
        assert item.id == "5"
        assert item.biller_id == "airng"
        assert item.payment_item_name == "AIRNG"
        assert item.currency_symbol == "NGN"
        assert item.is_amount_fixed == "false"

    def test_payment_request(self):
        """Test PaymentRequest model."""
        request = PaymentRequest(
            customer_id="09071046909",
            amount="1000",
            division="C",
            payment_item="airtime",
            product_id="423",
            biller_id="airng",
            reference="test-ref-123",
            phone_number="08012345678",
        )
        assert request.customer_id == "09071046909"
        assert request.amount == "1000"
        assert request.reference == "test-ref-123"

    def test_payment_response(self):
        """Test PaymentResponse model."""
        response = PaymentResponse(
            status="00",
            message="Successful payment",
            reference="test-ref-123",
            data={"key": "value"},
        )
        assert response.status == "00"
        assert response.message == "Successful payment"
        assert response.reference == "test-ref-123"
        assert response.data == {"key": "value"}

    def test_payment_response_without_data(self):
        """Test PaymentResponse model without data."""
        response = PaymentResponse(
            status="00", message="Successful payment", reference="test-ref-123"
        )
        assert response.data is None

    def test_transaction_status(self):
        """Test TransactionStatus model."""
        status = TransactionStatus(
            status="00",
            message="Successful Transaction Retrieval",
            transaction_status="00",
            amount="1000",
            token="12345",
        )
        assert status.status == "00"
        assert status.message == "Successful Transaction Retrieval"
        assert status.transaction_status == "00"
        assert status.amount == "1000"
        assert status.token == "12345"

    def test_transaction_status_minimal(self):
        """Test TransactionStatus model with minimal data."""
        status = TransactionStatus(status="108", message="No Transaction!")
        assert status.status == "108"
        assert status.message == "No Transaction!"
        assert status.transaction_status is None
        assert status.amount is None
        assert status.token is None

    def test_auth_token(self):
        """Test AuthToken model."""
        token = AuthToken(
            access_token="test_token",
            scope="am_application_scope default",
            token_type="Bearer",
            expires_in=9223372036854775807,
        )
        assert token.access_token == "test_token"
        assert token.scope == "am_application_scope default"
        assert token.token_type == "Bearer"
        assert token.expires_in == 9223372036854775807

    def test_api_response(self):
        """Test APIResponse model."""
        response = APIResponse(
            status="00", message="Success", data={"result": "data"}
        )
        assert response.status == "00"
        assert response.message == "Success"
        assert response.data == {"result": "data"}

    def test_api_response_without_data(self):
        """Test APIResponse model without data."""
        response = APIResponse(status="00", message="Success")
        assert response.data is None
