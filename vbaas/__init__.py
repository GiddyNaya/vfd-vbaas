"""
VBaaS Python SDK

A Python SDK for VFD Bank as a Service (VBaaS) API.
"""

from .client import VBaaSClient
from .exceptions import APIError, AuthenticationError, VBaaSError
from .models import (
    Biller,
    BillerCategory,
    BillerItem,
    PaymentRequest,
    PaymentResponse,
    TransactionStatus,
)

__version__ = "1.0.0"
__author__ = "VBaaS SDK"
__email__ = "support@example.com"

__all__ = [
    "VBaaSClient",
    "VBaaSError",
    "AuthenticationError",
    "APIError",
    "BillerCategory",
    "Biller",
    "BillerItem",
    "PaymentRequest",
    "PaymentResponse",
    "TransactionStatus",
]
