import pytest
from unittest.mock import patch, MagicMock

from kuhl_haus.bedrock.app.api_keys.default_key_auth import DefaultKeyAuth
from kuhl_haus.bedrock.app.api_keys.api_key_auth import ApiKeyAuth


@pytest.fixture
def mock_api_key_auth():
    """Fixture for mocking the parent ApiKeyAuth class."""
    with patch('kuhl_haus.bedrock.app.api_keys.default_key_auth.ApiKeyAuth') as mock:
        yield mock


def test_default_key_auth_initialization():
    """Test that DefaultKeyAuth initializes with the default API key."""
    # Arrange
    expected_api_key = "default-api-key"

    # Act
    with patch('kuhl_haus.bedrock.app.api_keys.default_key_auth.DEFAULT_API_KEY', expected_api_key):
        with patch('kuhl_haus.bedrock.app.api_keys.default_key_auth.ApiKeyAuth.__init__') as mock_init:
            mock_init.return_value = None
            sut = DefaultKeyAuth()

    # Assert
    mock_init.assert_called_once_with(api_key=expected_api_key)


def test_default_key_auth_is_valid_with_key_expect_true():
    """Test that is_valid returns True when api_key is not empty."""
    # Arrange
    with patch('kuhl_haus.bedrock.app.api_keys.default_key_auth.DEFAULT_API_KEY', "some-api-key"):
        sut = DefaultKeyAuth()

    # Act
    result = sut.is_valid()

    # Assert
    assert result is True


def test_default_key_auth_is_valid_with_empty_key_expect_false():
    """Test that is_valid returns False when api_key is empty."""
    # Arrange
    with patch('kuhl_haus.bedrock.app.api_keys.default_key_auth.DEFAULT_API_KEY', ""):
        sut = DefaultKeyAuth()

    # Act
    result = sut.is_valid()

    # Assert
    assert result is False


def test_default_key_auth_is_valid_with_none_key_expect_false():
    """Test that is_valid returns False when api_key is None."""
    # Arrange
    with patch('kuhl_haus.bedrock.app.api_keys.default_key_auth.DEFAULT_API_KEY', None):
        sut = DefaultKeyAuth()

    # Act
    result = sut.is_valid()

    # Assert
    assert result is False


@patch('kuhl_haus.bedrock.app.api_keys.default_key_auth.DEFAULT_API_KEY', "test-key")
def test_default_key_auth_inherits_from_api_key_auth():
    """Test that DefaultKeyAuth properly inherits from ApiKeyAuth."""
    # Arrange & Act
    sut = DefaultKeyAuth()

    # Assert
    assert isinstance(sut, ApiKeyAuth)
    assert sut.api_key == "test-key"


@patch('kuhl_haus.bedrock.app.api_keys.default_key_auth.DEFAULT_API_KEY', "")
def test_default_key_auth_with_falsy_values():
    """Test that DefaultKeyAuth handles various falsy values correctly."""
    # Arrange
    sut = DefaultKeyAuth()

    # Act & Assert - Check common falsy values
    with patch.object(sut, 'api_key', ""):
        assert sut.is_valid() is False

    with patch.object(sut, 'api_key', 0):
        assert sut.is_valid() is False

    with patch.object(sut, 'api_key', None):
        assert sut.is_valid() is False

    with patch.object(sut, 'api_key', False):
        assert sut.is_valid() is False


@patch('kuhl_haus.bedrock.app.api_keys.default_key_auth.DEFAULT_API_KEY', "test-key")
def test_default_key_auth_with_truthy_values():
    """Test that DefaultKeyAuth handles various truthy values correctly."""
    # Arrange
    sut = DefaultKeyAuth()

    # Act & Assert - Check common truthy values
    with patch.object(sut, 'api_key', "api-key"):
        assert sut.is_valid() is True

    with patch.object(sut, 'api_key', 1):
        assert sut.is_valid() is True

    with patch.object(sut, 'api_key', True):
        assert sut.is_valid() is True

    with patch.object(sut, 'api_key', [1, 2, 3]):
        assert sut.is_valid() is True
