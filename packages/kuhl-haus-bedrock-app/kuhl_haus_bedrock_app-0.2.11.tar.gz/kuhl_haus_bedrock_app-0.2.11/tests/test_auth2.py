import pytest
from unittest.mock import Mock, patch, create_autospec, MagicMock
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from kuhl_haus.bedrock.app.api_keys.api_key_auth import ApiKeyAuth

# import kuhl_haus.bedrock.app.auth2 as auth


@pytest.fixture
def valid_api_key():
    return "test-api-key"


@pytest.fixture
def invalid_api_key():
    return "invalid"


@pytest.fixture
def valid_credentials(valid_api_key):
    """Fixture for creating mock HTTPAuthorizationCredentials."""
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=valid_api_key)


@pytest.fixture
def invalid_credentials(invalid_api_key):
    """Fixture for creating mock HTTPAuthorizationCredentials."""
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=invalid_api_key)


@pytest.fixture
def mock_key_validator():
    """Fixture for mocking the key validator."""
    mock = MagicMock()
    return mock


class TestApiKeyAuth(ApiKeyAuth):
    """Concrete implementation of ApiKeyAuth for testing purposes."""
    def __init__(self, api_key: str):
        super().__init__(api_key=api_key)

    def is_valid(self) -> bool:
        return bool(self.api_key)


@patch('kuhl_haus.bedrock.app.factories.api_keys.get_api_key_validator')
def test_api_key_auth_valid_credentials(patched_get_key_validator, valid_credentials, valid_api_key):
    """Test api_key_auth with valid credentials."""
    # Arrange
    mock_validator = TestApiKeyAuth(api_key=valid_api_key)
    patched_get_key_validator.return_value = mock_validator

    # Act
    import kuhl_haus.bedrock.app.auth2 as auth
    result = auth.api_key_auth(credentials=valid_credentials)

    # Assert
    assert result is None  # Function returns None when successful


@patch('kuhl_haus.bedrock.app.factories.api_keys.get_api_key_validator')
def test_api_key_auth_invalid_credentials(patched_get_key_validator, invalid_credentials, valid_api_key):
    """Test api_key_auth with invalid credentials raises exception."""
    # Arrange
    mock_validator = TestApiKeyAuth(api_key=valid_api_key)
    patched_get_key_validator.return_value = mock_validator

    # Act & Assert
    import kuhl_haus.bedrock.app.auth2 as auth
    with pytest.raises(HTTPException) as excinfo:
        auth.api_key_auth(credentials=invalid_credentials)

    # Assert exception details
    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == "Invalid credentials"


@patch('kuhl_haus.bedrock.app.auth2.key_validator')
def test_api_key_auth_validator_exception(patched_key_validator, valid_credentials):
    """Test api_key_auth when validator raises an exception."""
    # Arrange
    patched_key_validator.validate_credentials.side_effect = Exception("Validator error")

    # Act & Assert
    import kuhl_haus.bedrock.app.auth2 as auth
    with pytest.raises(HTTPException) as excinfo:
        auth.api_key_auth(credentials=valid_credentials)

    # Assert exception details
    assert excinfo.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert excinfo.value.detail == "Validation error"
    patched_key_validator.validate_credentials.assert_called_once_with(valid_credentials)


@patch('kuhl_haus.bedrock.app.factories.api_keys.get_api_key_validator')
def test_api_key_auth_with_none_credentials(patched_get_key_validator, valid_api_key):
    """Test api_key_auth with None credentials."""
    # Arrange
    # Arrange
    mock_validator = TestApiKeyAuth(api_key=valid_api_key)
    patched_get_key_validator.return_value = mock_validator

    # Act & Assert
    import kuhl_haus.bedrock.app.auth2 as auth
    with pytest.raises(HTTPException) as excinfo:
        auth.api_key_auth(credentials=None)

    # Assert exception details
    assert excinfo.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert excinfo.value.detail == "Validation error"


@patch('kuhl_haus.bedrock.app.factories.api_keys.get_api_key_validator')
def test_module_initialization(patched_get_api_key_validator):
    """Test module initialization creates validator and security objects correctly."""
    # Arrange
    mock_validator = MagicMock()
    patched_get_api_key_validator.return_value = mock_validator

    # Act - Force module reimport to test initialization
    import importlib
    import kuhl_haus.bedrock.app.auth2 as auth
    importlib.reload(auth)

    # Assert
    patched_get_api_key_validator.assert_called_once()
    assert auth.key_validator == mock_validator
    assert isinstance(auth.security, auth.HTTPBearer)

