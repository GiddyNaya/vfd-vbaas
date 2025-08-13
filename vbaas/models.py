"""
VBaaS SDK Models

Data models for VBaaS API responses and requests.
"""

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Union


def serialize_models(
    models: Union[List[Any], Any],
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Serialize model objects or lists of model objects to dictionaries.

    Args:
        models: Single model object or list of model objects

    Returns:
        Dictionary or list of dictionaries ready for JSON serialization
    """
    if isinstance(models, list):
        result = []
        for model in models:
            if hasattr(model, "to_dict"):
                result.append(model.to_dict())
            else:
                result.append(model)
        return result
    else:
        if hasattr(models, "to_dict"):
            return models.to_dict()  # type: ignore[no-any-return]
        else:
            return models  # type: ignore[no-any-return]


@dataclass
class BillerCategory:
    """Represents a biller category."""

    category: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class Biller:
    """Represents a biller."""

    id: str
    name: str
    division: str
    product: str
    category: str
    convenience_fee: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


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

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


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

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class PaymentResponse:
    """Represents a payment response."""

    status: str
    message: str
    reference: str
    data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class TransactionStatus:
    """Represents transaction status."""

    status: str
    message: str
    transaction_status: Optional[str] = None
    amount: Optional[str] = None
    token: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class AuthToken:
    """Represents an authentication token."""

    access_token: str
    scope: str
    token_type: str
    expires_in: int

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


@dataclass
class APIResponse:
    """Generic API response wrapper."""

    status: str
    message: str
    data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)
