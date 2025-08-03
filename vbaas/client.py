"""
VBaaS Client

Main client class for interacting with VBaaS APIs.
"""

import time
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import requests

from .exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    NetworkError,
    ValidationError,
)
from .models import (
    Biller,
    BillerCategory,
    BillerItem,
    PaymentResponse,
    TransactionStatus,
)


class VBaaSClient:
    """
    VBaaS API Client

    Main client for interacting with VFD Bank as a Service APIs.
    """

    # Environment URLs
    ENVIRONMENTS = {
        "test": {
            "auth_base_url": (
                "https://api-devapps.vfdbank.systems/vfd-tech/baas-portal/v1.1"
            ),
            "bills_base_url": (
                "https://api-devapps.vfdbank.systems/vtech-bills/api/v2/"
                "billspaymentstore"
            ),
        },
        "live": {
            "auth_base_url": (
                "https://api-apps.vfdbank.systems/vfd-tech/baas-portal/v1.1"
            ),
            "bills_base_url": (
                "https://api-apps.vfdbank.systems/vtech-bills/api/v2/"
                "billspaymentstore"
            ),
        },
    }

    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        environment: str = "test",
        timeout: int = 30,
    ):
        """
        Initialize VBaaS client.

        Args:
            consumer_key: Your VBaaS consumer key
            consumer_secret: Your VBaaS consumer secret
            environment: Environment to use ('test' or 'live')
            timeout: Request timeout in seconds
        """
        if not consumer_key or not consumer_secret:
            raise ConfigurationError("Consumer key and secret are required")

        if environment not in self.ENVIRONMENTS:
            raise ConfigurationError(
                f"Invalid environment: {environment}. "
                f"Must be 'test' or 'live'"
            )

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.environment = environment
        self.timeout = timeout

        self.auth_base_url = self.ENVIRONMENTS[environment]["auth_base_url"]
        self.bills_base_url = self.ENVIRONMENTS[environment]["bills_base_url"]

        self._access_token: Optional[str] = None
        self._token_expires_at: Optional[float] = None

        # Initialize session
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _get_access_token(self) -> str:
        """Get or refresh access token."""
        if self._access_token and self._token_expires_at:
            # Check if token is still valid (with 5 minute buffer)
            if time.time() < (self._token_expires_at - 300):
                return self._access_token

        # Generate new token
        url = f"{self.auth_base_url}/baasauth/token"
        payload = {
            "consumerKey": self.consumer_key,
            "consumerSecret": self.consumer_secret,
            "validityTime": "-1",  # Non-expiring token
        }

        try:
            response = self.session.post(
                url, json=payload, timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()

            if data.get("status") != "00":
                raise AuthenticationError(
                    f"Authentication failed: "
                    f"{data.get('message', 'Unknown error')}"
                )

            token_data = data.get("data", {})
            self._access_token = token_data.get("access_token")

            if not self._access_token:
                raise AuthenticationError("No access token received")

            # Set expiration time (use expires_in if available,
            # otherwise set far future)
            expires_in = token_data.get("expires_in", 9223372036854775807)
            self._token_expires_at = time.time() + expires_in

            return self._access_token

        except requests.RequestException as e:
            raise NetworkError(f"Failed to authenticate: {str(e)}")

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        require_auth: bool = True,
    ) -> Dict[str, Any]:
        """Make authenticated API request."""
        url = urljoin(self.bills_base_url + "/", endpoint.lstrip("/"))

        headers = {}
        if require_auth:
            token = self._get_access_token()
            headers["Authorization"] = f"Bearer {token}"

        try:
            if method.upper() == "GET":
                response = self.session.get(
                    url, params=params, headers=headers, timeout=self.timeout
                )
            elif method.upper() == "POST":
                response = self.session.post(
                    url,
                    json=data,
                    params=params,
                    headers=headers,
                    timeout=self.timeout,
                )
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()  # type: ignore[no-any-return]

        except requests.RequestException as e:
            raise NetworkError(f"Request failed: {str(e)}")

    def _validate_response(
        self, response: Dict[str, Any], success_status: str = "00"
    ) -> Dict[str, Any]:
        """Validate API response."""
        status = response.get("status")
        message = response.get("message", "Unknown error")

        if status != success_status:
            raise APIError(message, status_code=status, response_data=response)

        return response

    # Bills Payment API Methods

    def get_biller_categories(self) -> List[BillerCategory]:
        """
        Get all available biller categories.

        Returns:
            List of biller categories
        """
        response = self._make_request("GET", "/billercategory")
        self._validate_response(response)

        categories_data = response.get("data", [])
        return [
            BillerCategory(category=item["category"])
            for item in categories_data
        ]

    def get_billers(self, category_name: str) -> List[Biller]:
        """
        Get billers for a specific category.

        Args:
            category_name: Name of the category

        Returns:
            List of billers
        """
        if not category_name:
            raise ValidationError("Category name is required")

        params = {"categoryName": category_name}
        response = self._make_request("GET", "/billerlist", params=params)
        self._validate_response(response)

        billers_data = response.get("data", [])
        billers = []

        for item in billers_data:
            biller = Biller(
                id=item["id"],
                name=item["name"],
                division=item["division"],
                product=item["product"],
                category=item["category"],
                convenience_fee=item.get("convenienceFee"),
            )
            billers.append(biller)

        return billers

    def get_biller_items(
        self, biller_id: str, division_id: str, product_id: str
    ) -> List[BillerItem]:
        """
        Get items for a specific biller.

        Args:
            biller_id: ID of the biller
            division_id: Division ID
            product_id: Product ID

        Returns:
            List of biller items
        """
        if not all([biller_id, division_id, product_id]):
            raise ValidationError(
                "Biller ID, division ID, and product ID are required"
            )

        params = {
            "billerId": biller_id,
            "divisionId": division_id,
            "productId": product_id,
        }
        response = self._make_request("GET", "/billerItems", params=params)
        self._validate_response(response)

        items_data = response.get("data", {}).get("paymentitems", [])
        biller_items = []

        for item in items_data:
            biller_item = BillerItem(
                id=item["id"],
                biller_id=item["billerid"],
                amount=item["amount"],
                code=item["code"],
                payment_item_name=item["paymentitemname"],
                product_id=item["productId"],
                payment_item_id=item["paymentitemid"],
                currency_symbol=item["currencySymbol"],
                is_amount_fixed=item["isAmountFixed"],
                item_fee=item["itemFee"],
                item_currency_symbol=item["itemCurrencySymbol"],
                picture_id=item["pictureId"],
                payment_code=item["paymentCode"],
                sort_order=item["sortOrder"],
                biller_type=item["billerType"],
                pay_direct_item_code=item["payDirectitemCode"],
                currency_code=item["currencyCode"],
                division=item["division"],
                category_id=item["categoryid"],
                created_date=item["createdDate"],
            )
            biller_items.append(biller_item)

        return biller_items

    def validate_customer(
        self,
        division_id: str,
        payment_item: str,
        customer_id: str,
        biller_id: str,
    ) -> bool:
        """
        Validate customer information.

        Args:
            division_id: Division ID
            payment_item: Payment item
            customer_id: Customer ID to validate
            biller_id: Biller ID

        Returns:
            True if validation successful
        """
        if not all([division_id, payment_item, customer_id, biller_id]):
            raise ValidationError(
                "All parameters are required for customer validation"
            )

        params = {
            "divisionId": division_id,
            "paymentItem": payment_item,
            "customerId": customer_id,
            "billerId": biller_id,
        }

        response = self._make_request(
            "GET", "/customervalidate", params=params
        )
        self._validate_response(response)

        return True

    def pay_bill(
        self,
        customer_id: str,
        amount: str,
        division: str,
        payment_item: str,
        product_id: str,
        biller_id: str,
        reference: str,
        phone_number: str,
    ) -> PaymentResponse:
        """
        Make a bill payment.

        Args:
            customer_id: Customer ID
            amount: Payment amount
            division: Division
            payment_item: Payment item
            product_id: Product ID
            biller_id: Biller ID
            reference: Unique payment reference
            phone_number: Customer phone number

        Returns:
            Payment response
        """
        if not all(
            [
                customer_id,
                amount,
                division,
                payment_item,
                product_id,
                biller_id,
                reference,
                phone_number,
            ]
        ):
            raise ValidationError("All payment parameters are required")

        payload = {
            "customerId": customer_id,
            "amount": amount,
            "division": division,
            "paymentItem": payment_item,
            "productId": product_id,
            "billerId": biller_id,
            "reference": reference,
            "phoneNumber": phone_number,
        }

        response = self._make_request("POST", "/pay", data=payload)

        # Payment can return status "00" for success or "99" for failure
        status = response.get("status")
        message = response.get("message", "Unknown error")
        reference_returned = response.get("data", {}).get(
            "reference", reference
        )

        return PaymentResponse(
            status=str(status) if status is not None else "99",
            message=message,
            reference=reference_returned,
            data=response.get("data"),
        )

    def get_transaction_status(self, transaction_id: str) -> TransactionStatus:
        """
        Get transaction status.

        Args:
            transaction_id: Transaction ID to check

        Returns:
            Transaction status
        """
        if not transaction_id:
            raise ValidationError("Transaction ID is required")

        params = {"transactionId": transaction_id}
        response = self._make_request(
            "GET", "/transactionStatus", params=params
        )

        # Handle different response statuses
        status = response.get("status")
        message = response.get("message", "Unknown error")

        if status == "108":  # No transaction found
            return TransactionStatus(
                status=str(status) if status is not None else "99",
                message=message,
            )

        # Validate successful response
        self._validate_response(response)

        data = response.get("data", {})
        return TransactionStatus(
            status=str(status) if status is not None else "99",
            message=message,
            transaction_status=data.get("transactionStatus"),
            amount=data.get("amount"),
            token=data.get("token"),
        )

    def close(self) -> None:
        """Close the HTTP session."""
        if hasattr(self, "session"):
            self.session.close()
