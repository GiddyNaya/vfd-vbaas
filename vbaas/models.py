"""
VBaaS SDK Models

Data models for VBaaS API responses and requests.
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class BillerCategory:
    """Represents a biller category."""

    category: str


@dataclass
class Biller:
    """Represents a biller."""

    id: str
    name: str
    division: str
    product: str
    category: str
    convenience_fee: Optional[str] = None


@dataclass
class BillerItem:
    """Represents a biller item."""

    id: str
    biller_id: str
    amount: str
    code: str
    payment_item_name: str
    product_id: str
    payment_item_id: str
    currency_symbol: str
    is_amount_fixed: str
    item_fee: str
    item_currency_symbol: str
    picture_id: str
    payment_code: str
    sort_order: str
    biller_type: str
    pay_direct_item_code: str
    currency_code: str
    division: str
    category_id: str
    created_date: str


@dataclass
class PaymentRequest:
    """Represents a payment request."""

    customer_id: str
    amount: str
    division: str
    payment_item: str
    product_id: str
    biller_id: str
    reference: str
    phone_number: str


@dataclass
class PaymentResponse:
    """Represents a payment response."""

    status: str
    message: str
    reference: str
    data: Optional[Dict[str, Any]] = None


@dataclass
class TransactionStatus:
    """Represents transaction status."""

    status: str
    message: str
    transaction_status: Optional[str] = None
    amount: Optional[str] = None
    token: Optional[str] = None


@dataclass
class AuthToken:
    """Represents an authentication token."""

    access_token: str
    scope: str
    token_type: str
    expires_in: int


@dataclass
class APIResponse:
    """Generic API response wrapper."""

    status: str
    message: str
    data: Optional[Dict[str, Any]] = None
