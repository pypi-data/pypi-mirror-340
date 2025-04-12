import pytest
from unittest.mock import Mock, create_autospec
from typing import Union
from fastapi.security import HTTPAuthorizationCredentials

from kuhl_haus.bedrock.app.api_keys.api_key_auth import ApiKeyAuth


class ConcreteApiKeyAuth(ApiKeyAuth):
    """Concrete implementation of ApiKeyAuth for testing purposes."""

    def is_valid(self) -> bool:
        return bool(self.api_key)


@pytest.fixture
def valid_api_key():
    return "valid-api-key-12345"


@pytest.fixture
def mock_credentials():
    """Creates a mock HTTPAuthorizationCredentials object."""
    mock = create_autospec(HTTPAuthorizationCredentials)
    mock.credentials = None
    return mock


def test_init_with_api_key(valid_api_key):
    """Test that the class initializes correctly with an API key."""
    # Arrange & Act
    sut = ConcreteApiKeyAuth(api_key=valid_api_key)

    # Assert
    assert sut.api_key == valid_api_key


def test_init_without_api_key():
    """Test that the class initializes correctly without an API key."""
    # Arrange & Act
    sut = ConcreteApiKeyAuth()

    # Assert
    assert sut.api_key is None


def test_is_valid_abstract_method():
    """Test that using is_valid on the abstract class raises NotImplementedError."""

    # Arrange
    class TestAbstractClass(ApiKeyAuth):
        pass

    # Act & Assert
    with pytest.raises(TypeError, match="Can't instantiate abstract class TestAbstractClass without an implementation for abstract method"):
        TestAbstractClass()


def test_validate_credentials_matching_key(valid_api_key, mock_credentials):
    """Test that validate_credentials returns True when credentials match the API key."""
    # Arrange
    sut = ConcreteApiKeyAuth(api_key=valid_api_key)
    mock_credentials.credentials = valid_api_key

    # Act
    result = sut.validate_credentials(mock_credentials)

    # Assert
    assert result is True


def test_validate_credentials_non_matching_key(valid_api_key, mock_credentials):
    """Test that validate_credentials returns False when credentials don't match the API key."""
    # Arrange
    sut = ConcreteApiKeyAuth(api_key=valid_api_key)
    mock_credentials.credentials = "wrong-api-key"

    # Act
    result = sut.validate_credentials(mock_credentials)

    # Assert
    assert result is False


def test_validate_credentials_with_none_api_key(mock_credentials):
    """Test validate_credentials when the API key is None."""
    # Arrange
    sut = ConcreteApiKeyAuth(api_key=None)
    mock_credentials.credentials = "some-api-key"

    # Act
    result = sut.validate_credentials(mock_credentials)

    # Assert
    assert result is False


def test_validate_credentials_with_none_credentials():
    """Test validate_credentials with None credentials parameter."""
    # Arrange
    sut = ConcreteApiKeyAuth(api_key="some-key")

    # Act & Assert
    with pytest.raises(AttributeError):
        sut.validate_credentials(None)


def test_validate_credentials_with_empty_credentials_value(mock_credentials):
    """Test validate_credentials with empty string as credentials value."""
    # Arrange
    sut = ConcreteApiKeyAuth(api_key="some-key")
    mock_credentials.credentials = ""

    # Act
    result = sut.validate_credentials(mock_credentials)

    # Assert
    assert result is False


def test_validate_credentials_with_empty_api_key(mock_credentials):
    """Test validate_credentials with empty string as API key."""
    # Arrange
    sut = ConcreteApiKeyAuth(api_key="")
    mock_credentials.credentials = "some-key"

    # Act
    result = sut.validate_credentials(mock_credentials)

    # Assert
    assert result is False


def test_concrete_is_valid_with_valid_key(valid_api_key):
    """Test that a concrete implementation returns True for a valid API key."""
    # Arrange
    sut = ConcreteApiKeyAuth(api_key=valid_api_key)

    # Act
    result = sut.is_valid()

    # Assert
    assert result is True


def test_concrete_is_valid_with_none_key():
    """Test that a concrete implementation returns False for a None API key."""
    # Arrange
    sut = ConcreteApiKeyAuth(api_key=None)

    # Act
    result = sut.is_valid()

    # Assert
    assert result is False


def test_concrete_is_valid_with_empty_key():
    """Test that a concrete implementation returns False for an empty API key."""
    # Arrange
    sut = ConcreteApiKeyAuth(api_key="")

    # Act
    result = sut.is_valid()

    # Assert
    assert result is False
