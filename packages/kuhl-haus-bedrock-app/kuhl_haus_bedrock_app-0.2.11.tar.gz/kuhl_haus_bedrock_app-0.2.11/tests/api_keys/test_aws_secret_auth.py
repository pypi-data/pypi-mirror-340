import pytest
from unittest.mock import patch, MagicMock

from kuhl_haus.bedrock.app.api_keys.aws_secret_auth import AwsSecretAuth
from kuhl_haus.bedrock.app.api_keys.api_key_auth import ApiKeyAuth


@pytest.fixture
def mock_ssm_parameter():
    with patch("kuhl_haus.bedrock.app.api_keys.aws_secret_auth.get_ssm_parameter") as mock:
        yield mock


@pytest.fixture
def mock_secret_string():
    with patch("kuhl_haus.bedrock.app.api_keys.aws_secret_auth.get_secret_string") as mock:
        yield mock


@pytest.fixture
def mock_api_key_auth_init():
    with patch.object(ApiKeyAuth, "__init__", return_value=None) as mock:
        yield mock


@patch("kuhl_haus.bedrock.app.api_keys.aws_secret_auth.SECRET_ARN_PARAMETER", "test-parameter")
def test_init_with_secret_arn_parameter(mock_ssm_parameter, mock_secret_string, mock_api_key_auth_init):
    """Test initialization when SECRET_ARN_PARAMETER is set."""
    # Arrange
    secret_arn = "arn:aws:secretsmanager:us-west-2:123456789012:secret:test-secret"
    api_key_value = "test-api-key"
    mock_ssm_parameter.return_value = secret_arn
    mock_secret_string.return_value = api_key_value

    # Act
    sut = AwsSecretAuth()

    # Assert
    assert sut.api_key_secret_arn == secret_arn
    mock_ssm_parameter.assert_called_once_with(parameter_name="test-parameter")
    mock_secret_string.assert_called_once_with(arn=secret_arn)
    mock_api_key_auth_init.assert_called_once_with(api_key=api_key_value)


@patch("kuhl_haus.bedrock.app.api_keys.aws_secret_auth.SECRET_ARN_PARAMETER", None)
def test_init_without_secret_arn_parameter(mock_ssm_parameter, mock_secret_string, mock_api_key_auth_init):
    """Test initialization when SECRET_ARN_PARAMETER is not set."""
    # Arrange
    # Act
    sut = AwsSecretAuth()

    # Assert
    assert sut.api_key_secret_arn is None
    mock_ssm_parameter.assert_not_called()
    mock_secret_string.assert_not_called()
    mock_api_key_auth_init.assert_called_once_with(api_key=None)


@patch("kuhl_haus.bedrock.app.api_keys.aws_secret_auth.SECRET_ARN_PARAMETER", "test-parameter")
def test_is_valid_with_secret_arn(mock_ssm_parameter, mock_secret_string, mock_api_key_auth_init):
    """Test is_valid returns True when api_key_secret_arn is set."""
    # Arrange
    secret_arn = "arn:aws:secretsmanager:us-west-2:123456789012:secret:test-secret"
    mock_ssm_parameter.return_value = secret_arn
    mock_secret_string.return_value = "test-api-key"
    sut = AwsSecretAuth()

    # Act
    result = sut.is_valid()

    # Assert
    assert result is True


@patch("kuhl_haus.bedrock.app.api_keys.aws_secret_auth.SECRET_ARN_PARAMETER", None)
def test_is_valid_without_secret_arn(mock_ssm_parameter, mock_secret_string, mock_api_key_auth_init):
    """Test is_valid returns False when api_key_secret_arn is None."""
    # Arrange
    sut = AwsSecretAuth()

    # Act
    result = sut.is_valid()

    # Assert
    assert result is False


@patch("kuhl_haus.bedrock.app.api_keys.aws_secret_auth.SECRET_ARN_PARAMETER", "test-parameter")
def test_empty_secret_arn_from_ssm(mock_ssm_parameter, mock_secret_string, mock_api_key_auth_init):
    """Test handling when SSM returns empty string for secret ARN."""
    # Arrange
    mock_ssm_parameter.return_value = ""
    mock_secret_string.return_value = None

    # Act
    sut = AwsSecretAuth()
    result = sut.is_valid()

    # Assert
    assert sut.api_key_secret_arn == ""
    assert result is False  # Empty string converts to False with bool()
    mock_secret_string.assert_called_once_with(arn="")


@patch("kuhl_haus.bedrock.app.api_keys.aws_secret_auth.SECRET_ARN_PARAMETER", "test-parameter")
def test_ssm_parameter_error_handling(mock_ssm_parameter, mock_secret_string, mock_api_key_auth_init):
    """Test handling when SSM parameter fetch raises an exception."""
    # Arrange
    mock_ssm_parameter.side_effect = Exception("SSM parameter fetch failed")

    # Act & Assert
    with pytest.raises(Exception, match="SSM parameter fetch failed"):
        AwsSecretAuth()
    mock_secret_string.assert_not_called()


@patch("kuhl_haus.bedrock.app.api_keys.aws_secret_auth.SECRET_ARN_PARAMETER", "test-parameter")
def test_secret_string_error_handling(mock_ssm_parameter, mock_secret_string, mock_api_key_auth_init):
    """Test handling when secret string fetch raises an exception."""
    # Arrange
    mock_ssm_parameter.return_value = "secret-arn"
    mock_secret_string.side_effect = Exception("Secret fetch failed")

    # Act & Assert
    with pytest.raises(Exception, match="Secret fetch failed"):
        AwsSecretAuth()
    mock_ssm_parameter.assert_called_once()
