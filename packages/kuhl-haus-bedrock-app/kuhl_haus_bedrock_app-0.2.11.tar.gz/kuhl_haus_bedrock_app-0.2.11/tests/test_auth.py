from unittest.mock import patch, MagicMock

import pytest
from fastapi import HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from kuhl_haus.bedrock.app.env import SECRET_ARN_PARAMETER


@pytest.fixture
def mock_credentials():
    """Fixture for mock credentials"""
    credentials = MagicMock(spec=HTTPAuthorizationCredentials)
    credentials.credentials = "test-api-key"
    return credentials


@pytest.fixture
def reset_module_state():
    """Fixture to reset module-level state between tests"""
    # Store original module to restore after test
    import sys
    if 'kuhl_haus.bedrock.app.auth' in sys.modules:
        original_module = sys.modules['kuhl_haus.bedrock.app.auth']
        del sys.modules['kuhl_haus.bedrock.app.auth']
    else:
        original_module = None

    yield

    # Restore original module if it existed
    if original_module:
        sys.modules['kuhl_haus.bedrock.app.auth'] = original_module


@patch('kuhl_haus.bedrock.app.helpers.parameter_store_helper.get_ssm_parameter')
@patch('kuhl_haus.bedrock.app.helpers.secrets_manager_helper.get_secret_string')
def test_module_initialization(mock_get_secret_string, mock_get_ssm_parameter, reset_module_state):
    """Test module initialization fetches secrets correctly"""
    # Arrange
    mock_get_ssm_parameter.return_value = "mock-secret-arn"
    mock_get_secret_string.return_value = "mock-api-key"

    # Act - Import the module fresh
    import kuhl_haus.bedrock.app.auth as auth_module

    # Assert
    mock_get_ssm_parameter.assert_called_once_with(parameter_name=SECRET_ARN_PARAMETER)
    mock_get_secret_string.assert_called_once_with(arn="mock-secret-arn")
    assert auth_module.api_key == "mock-api-key"
    assert auth_module.api_key_secret_arn == "mock-secret-arn"


@patch('kuhl_haus.bedrock.app.helpers.parameter_store_helper.get_ssm_parameter')
@patch('kuhl_haus.bedrock.app.helpers.secrets_manager_helper.get_secret_string')
def test_api_key_auth_with_valid_credentials(
        mock_get_secret_string,
        mock_get_ssm_parameter,
        mock_credentials,
        reset_module_state
):
    """Test api_key_auth accepts valid credentials"""
    # Arrange
    mock_get_ssm_parameter.return_value = "mock-secret-arn"
    mock_get_secret_string.return_value = "test-api-key"

    # Import the module after mocking
    import kuhl_haus.bedrock.app.auth as auth_module

    # Act
    result = auth_module.api_key_auth(mock_credentials)

    # Assert
    assert result is None  # Function returns None when successful


@patch('kuhl_haus.bedrock.app.helpers.parameter_store_helper.get_ssm_parameter')
@patch('kuhl_haus.bedrock.app.helpers.secrets_manager_helper.get_secret_string')
def test_api_key_auth_with_invalid_credentials(
        mock_get_secret_string,
        mock_get_ssm_parameter,
        mock_credentials,
        reset_module_state
):
    """Test api_key_auth rejects invalid credentials"""
    # Arrange
    mock_get_ssm_parameter.return_value = "mock-secret-arn"
    mock_get_secret_string.return_value = "correct-api-key"

    # Import the module after mocking
    import kuhl_haus.bedrock.app.auth as auth_module
    mock_credentials.credentials = "wrong-api-key"

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        auth_module.api_key_auth(mock_credentials)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid API Key"


@patch('kuhl_haus.bedrock.app.helpers.parameter_store_helper.get_ssm_parameter')
@patch('kuhl_haus.bedrock.app.helpers.secrets_manager_helper.get_secret_string')
def test_api_key_auth_with_empty_credentials(
        mock_get_secret_string,
        mock_get_ssm_parameter,
        mock_credentials,
        reset_module_state
):
    """Test api_key_auth rejects empty credentials"""
    # Arrange
    mock_get_ssm_parameter.return_value = "mock-secret-arn"
    mock_get_secret_string.return_value = "correct-api-key"

    # Import the module after mocking
    import kuhl_haus.bedrock.app.auth as auth_module
    mock_credentials.credentials = ""

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        auth_module.api_key_auth(mock_credentials)

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Invalid API Key"


@patch('kuhl_haus.bedrock.app.helpers.parameter_store_helper.get_ssm_parameter')
@patch('kuhl_haus.bedrock.app.helpers.secrets_manager_helper.get_secret_string')
def test_module_handles_missing_parameter(
        mock_get_secret_string,
        mock_get_ssm_parameter,
        reset_module_state
):
    """Test module handles missing SSM parameter"""
    # Arrange
    mock_get_ssm_parameter.side_effect = RuntimeError("Parameter not found")
    mock_get_secret_string.side_effect = TypeError("Expected error when arn is None")

    # Act & Assert
    with pytest.raises(RuntimeError):
        import kuhl_haus.bedrock.app.auth  # noqa - import is not used, obviously.

    mock_get_ssm_parameter.assert_called_once_with(parameter_name=SECRET_ARN_PARAMETER)
    # get_secret_string should not be called if get_ssm_parameter returns None
    mock_get_secret_string.assert_not_called()


@patch('kuhl_haus.bedrock.app.helpers.parameter_store_helper.get_ssm_parameter')
@patch('kuhl_haus.bedrock.app.helpers.secrets_manager_helper.get_secret_string')
def test_module_handles_missing_secret(
        mock_get_secret_string,
        mock_get_ssm_parameter,
        reset_module_state
):
    """Test module handles missing secret"""
    # Arrange
    mock_get_ssm_parameter.return_value = "mock-secret-arn"
    mock_get_secret_string.return_value = None

    # Act - importing should set api_key to None
    import kuhl_haus.bedrock.app.auth as auth_module

    # Assert
    mock_get_ssm_parameter.assert_called_once_with(parameter_name=SECRET_ARN_PARAMETER)
    mock_get_secret_string.assert_called_once_with(arn="mock-secret-arn")
    assert auth_module.api_key is None


@patch('fastapi.security.HTTPBearer')
@patch('kuhl_haus.bedrock.app.helpers.parameter_store_helper.get_ssm_parameter')
@patch('kuhl_haus.bedrock.app.helpers.secrets_manager_helper.get_secret_string')
def test_security_instance_creation(
        mock_get_secret_string,
        mock_get_ssm_parameter,
        mock_http_bearer,
        reset_module_state
):
    """Test security instance is created correctly"""
    # Arrange
    mock_get_ssm_parameter.return_value = "mock-secret-arn"
    mock_get_secret_string.return_value = "mock-api-key"
    mock_instance = MagicMock()
    mock_http_bearer.return_value = mock_instance

    # Act
    import kuhl_haus.bedrock.app.auth as auth_module

    # Assert
    mock_http_bearer.assert_called_once()
    assert auth_module.security is mock_instance
