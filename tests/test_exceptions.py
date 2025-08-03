"""
Tests for VBaaS Exceptions

Unit tests for the VBaaS Python SDK exceptions.
"""

from vbaas.exceptions import (
    APIError,
    AuthenticationError,
    ConfigurationError,
    NetworkError,
    ValidationError,
    VBaaSError,
)


class TestExceptions:
    """Test cases for VBaaS exceptions."""

    def test_vbaas_error_basic(self):
        """Test basic VBaaSError."""
        error = VBaaSError("Test error")
        assert str(error) == "Test error"
        assert error.message == "Test error"
        assert error.status_code is None
        assert error.response_data == {}

    def test_vbaas_error_with_status_code(self):
        """Test VBaaSError with status code."""
        error = VBaaSError("Test error", status_code="99")
        assert error.message == "Test error"
        assert error.status_code == "99"

    def test_vbaas_error_with_response_data(self):
        """Test VBaaSError with response data."""
        response_data = {"key": "value", "error": "details"}
        error = VBaaSError("Test error", response_data=response_data)
        assert error.response_data == response_data

    def test_authentication_error(self):
        """Test AuthenticationError."""
        error = AuthenticationError()
        assert error.message == "Authentication failed"
        assert isinstance(error, VBaaSError)

    def test_authentication_error_custom_message(self):
        """Test AuthenticationError with custom message."""
        error = AuthenticationError("Invalid credentials")
        assert error.message == "Invalid credentials"

    def test_api_error(self):
        """Test APIError."""
        error = APIError("API request failed", status_code="99")
        assert error.message == "API request failed"
        assert error.status_code == "99"
        assert isinstance(error, VBaaSError)

    def test_validation_error(self):
        """Test ValidationError."""
        error = ValidationError("Invalid input")
        assert error.message == "Invalid input"
        assert isinstance(error, VBaaSError)

    def test_network_error(self):
        """Test NetworkError."""
        error = NetworkError()
        assert error.message == "Network request failed"
        assert isinstance(error, VBaaSError)

    def test_network_error_custom_message(self):
        """Test NetworkError with custom message."""
        error = NetworkError("Connection timeout")
        assert error.message == "Connection timeout"

    def test_configuration_error(self):
        """Test ConfigurationError."""
        error = ConfigurationError()
        assert error.message == "Invalid configuration"
        assert isinstance(error, VBaaSError)

    def test_configuration_error_custom_message(self):
        """Test ConfigurationError with custom message."""
        error = ConfigurationError("Missing API key")
        assert error.message == "Missing API key"

    def test_exception_inheritance(self):
        """Test exception inheritance hierarchy."""
        assert issubclass(AuthenticationError, VBaaSError)
        assert issubclass(APIError, VBaaSError)
        assert issubclass(ValidationError, VBaaSError)
        assert issubclass(NetworkError, VBaaSError)
        assert issubclass(ConfigurationError, VBaaSError)
        assert issubclass(VBaaSError, Exception)
