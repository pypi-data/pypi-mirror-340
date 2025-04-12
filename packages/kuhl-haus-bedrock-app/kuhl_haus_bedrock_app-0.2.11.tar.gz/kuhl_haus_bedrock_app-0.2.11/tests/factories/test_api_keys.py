import pytest
from unittest.mock import patch, MagicMock

from kuhl_haus.bedrock.app.factories.api_keys import get_api_key_validator
from kuhl_haus.bedrock.app.api_keys.aws_secret_auth import AwsSecretAuth
from kuhl_haus.bedrock.app.api_keys.default_key_auth import DefaultKeyAuth


@patch('kuhl_haus.bedrock.app.factories.api_keys.AwsSecretAuth')
@patch('kuhl_haus.bedrock.app.factories.api_keys.DefaultKeyAuth')
def test_get_api_key_validator_returns_aws_auth_when_valid(
        mock_default_key_auth,
        mock_aws_secret_auth
):
    """Test that AWS Secret Auth is returned when it's valid."""
    # Arrange
    mock_aws_instance = MagicMock()
    mock_aws_instance.is_valid.return_value = True
    mock_aws_secret_auth.return_value = mock_aws_instance

    # Act
    result = get_api_key_validator()

    # Assert
    assert result == mock_aws_instance
    mock_aws_instance.is_valid.assert_called_once()
    mock_default_key_auth.assert_not_called()


@patch('kuhl_haus.bedrock.app.factories.api_keys.AwsSecretAuth')
@patch('kuhl_haus.bedrock.app.factories.api_keys.DefaultKeyAuth')
def test_get_api_key_validator_returns_default_auth_when_aws_invalid(
        mock_default_key_auth,
        mock_aws_secret_auth
):
    """Test that DefaultKeyAuth is returned when AWS auth is invalid but Default auth is valid."""
    # Arrange
    mock_aws_instance = MagicMock()
    mock_aws_instance.is_valid.return_value = False
    mock_aws_secret_auth.return_value = mock_aws_instance

    mock_default_instance = MagicMock()
    mock_default_instance.is_valid.return_value = True
    mock_default_key_auth.return_value = mock_default_instance

    # Act
    result = get_api_key_validator()

    # Assert
    assert result == mock_default_instance
    mock_aws_instance.is_valid.assert_called_once()
    mock_default_instance.is_valid.assert_called_once()


@patch('kuhl_haus.bedrock.app.factories.api_keys.AwsSecretAuth')
@patch('kuhl_haus.bedrock.app.factories.api_keys.DefaultKeyAuth')
def test_get_api_key_validator_raises_error_when_both_invalid(
        mock_default_key_auth,
        mock_aws_secret_auth
):
    """Test that RuntimeError is raised when no valid auth methods are found."""
    # Arrange
    mock_aws_instance = MagicMock()
    mock_aws_instance.is_valid.return_value = False
    mock_aws_secret_auth.return_value = mock_aws_instance

    mock_default_instance = MagicMock()
    mock_default_instance.is_valid.return_value = False
    mock_default_key_auth.return_value = mock_default_instance

    # Act & Assert
    with pytest.raises(RuntimeError) as excinfo:
        get_api_key_validator()

    assert "No valid API key found" in str(excinfo.value)
    mock_aws_instance.is_valid.assert_called_once()
    mock_default_instance.is_valid.assert_called_once()


@patch('kuhl_haus.bedrock.app.factories.api_keys.AwsSecretAuth')
def test_get_api_key_validator_handles_aws_auth_exception(mock_aws_secret_auth):
    """Test that the function handles exceptions from AwsSecretAuth."""
    # Arrange
    mock_aws_secret_auth.side_effect = Exception("AWS Auth Error")

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        get_api_key_validator()

    assert "AWS Auth Error" in str(excinfo.value)


@patch('kuhl_haus.bedrock.app.factories.api_keys.AwsSecretAuth')
@patch('kuhl_haus.bedrock.app.factories.api_keys.DefaultKeyAuth')
def test_get_api_key_validator_handles_default_auth_exception(
        mock_default_key_auth,
        mock_aws_secret_auth
):
    """Test that the function handles exceptions from DefaultKeyAuth."""
    # Arrange
    mock_aws_instance = MagicMock()
    mock_aws_instance.is_valid.return_value = False
    mock_aws_secret_auth.return_value = mock_aws_instance

    mock_default_key_auth.side_effect = Exception("Default Auth Error")

    # Act & Assert
    with pytest.raises(Exception) as excinfo:
        get_api_key_validator()

    assert "Default Auth Error" in str(excinfo.value)
    mock_aws_instance.is_valid.assert_called_once()
