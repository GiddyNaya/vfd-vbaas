"""
VBaaS SDK Exceptions

Custom exception classes for the VBaaS Python SDK.
"""

from typing import Any, Dict, Optional


class VBaaSError(Exception):
    """Base exception class for VBaaS SDK errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[str] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}


class AuthenticationError(VBaaSError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed", **kwargs: Any):
        super().__init__(message, **kwargs)


class APIError(VBaaSError):
    """Raised when API request fails."""

    def __init__(
        self, message: str, status_code: Optional[str] = None, **kwargs: Any
    ):
        super().__init__(message, status_code, **kwargs)


class ValidationError(VBaaSError):
    """Raised when request validation fails."""

    def __init__(self, message: str, **kwargs: Any):
        super().__init__(message, **kwargs)


class NetworkError(VBaaSError):
    """Raised when network request fails."""

    def __init__(self, message: str = "Network request failed", **kwargs: Any):
        super().__init__(message, **kwargs)


class ConfigurationError(VBaaSError):
    """Raised when SDK configuration is invalid."""

    def __init__(self, message: str = "Invalid configuration", **kwargs: Any):
        super().__init__(message, **kwargs)
