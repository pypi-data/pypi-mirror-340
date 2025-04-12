import uuid
from random import choice
from unittest.mock import MagicMock, patch

import pytest

from kuhl_haus.bedrock.app.helpers.secrets_manager_helper import get_secret_string


def get_pseudorandom_arn():
    # Generate a fake ARN from a UUID so lru_cache doesn't skew results
    choices_string = uuid.uuid4().hex
    arn = ""
    for x in range(0, 32):
        arn = arn + choice(choices_string)
    return arn


@pytest.fixture()
def valid_arn():
    return get_pseudorandom_arn()


@pytest.fixture()
def valid_secret_string():
    return "valid_secret"


@pytest.fixture()
def valid_get_secret_value_response(valid_secret_string):
    response = {"SecretString": valid_secret_string}
    return response


@pytest.fixture()
def mock_sm_client(valid_get_secret_value_response):
    mock = MagicMock()
    mock.get_secret_value = MagicMock()
    mock.get_secret_value.return_value = valid_get_secret_value_response
    return mock


def test_get_secret_string_happy_path(mock_sm_client, valid_arn, valid_secret_string):
    # Arrange
    with patch("kuhl_haus.bedrock.app.helpers.secrets_manager_helper.aws_client_factory") as cf:
        expected_result = valid_secret_string
        cf.get_client_for_service.return_value = mock_sm_client
        sut = get_secret_string

        # Act
        result = sut(valid_arn)

    # Assert
    assert expected_result == result


def test_get_secret_string_with_positive_cache_hit_happy_path(
    mock_sm_client, valid_arn, valid_secret_string, valid_get_secret_value_response
):
    # Arrange
    with patch("kuhl_haus.bedrock.app.helpers.secrets_manager_helper.aws_client_factory") as cf:
        expected_result = valid_secret_string
        cf.get_client_for_service.return_value = mock_sm_client
        sut = get_secret_string

        # Act
        cache_info_0 = sut.cache_info()
        print(cache_info_0)

        result1 = sut(valid_arn)
        cache_info_1 = sut.cache_info()
        print(cache_info_1)

        result2 = sut(valid_arn)
        cache_info_2 = sut.cache_info()
        print(cache_info_2)

    # Assert
    assert expected_result == result1
    assert expected_result == result2
    # CacheInfo is a tuple:
    # hits, misses, max_size, current_size = cache_info_n
    assert cache_info_0[3] < cache_info_1[3]  # assert cache size increased
    assert cache_info_1[3] == cache_info_2[3]  # assert cache size did not increase
    assert cache_info_2[0] > cache_info_1[0]  # assert hits increased
    assert cache_info_2[1] == cache_info_1[1]  # assert misses did not increase


def test_get_secret_string_with_negative_cache_hit_happy_path(
    mock_sm_client, valid_arn, valid_secret_string, valid_get_secret_value_response
):
    # Arrange
    with patch("kuhl_haus.bedrock.app.helpers.secrets_manager_helper.aws_client_factory") as cf:
        expected_result = valid_secret_string
        cf.get_client_for_service.return_value = mock_sm_client
        sut = get_secret_string

        # Act
        cache_info_0 = sut.cache_info()
        print(cache_info_0)

        result1 = sut(valid_arn)
        cache_info_1 = sut.cache_info()
        print(cache_info_1)

        result2 = sut(get_pseudorandom_arn())
        cache_info_2 = sut.cache_info()
        print(cache_info_2)

    # Assert
    assert expected_result == result1
    assert expected_result == result2
    # CacheInfo is a tuple:
    # hits, misses, max_size, current_size = cache_info_n
    assert cache_info_0[3] < cache_info_1[3]  # assert cache size increased
    assert cache_info_1[3] < cache_info_2[3]  # assert cache size increased
    assert cache_info_2[0] == cache_info_1[0]  # assert hits did not increase
    assert cache_info_2[1] > cache_info_1[1]  # assert misses increased


def test_get_secret_string_with_invalid_response_expect_runtime_error(valid_arn):
    # Arrange
    with patch("kuhl_haus.bedrock.app.helpers.secrets_manager_helper.aws_client_factory") as cf:
        sm_client = MagicMock()
        sm_client.get_secret_value = MagicMock()
        sm_client.get_secret_value.return_value = {}
        cf.get_client_for_service.return_value = sm_client
        with pytest.raises(RuntimeError) as e:
            # Act
            _ = get_secret_string(valid_arn)

    # Assert
    assert e.match(regexp=".*SecretString.*")


def test_get_secret_string_with_unhandled_exception_expect_runtime_error(valid_arn):
    # Arrange
    with patch("kuhl_haus.bedrock.app.helpers.secrets_manager_helper.aws_client_factory") as cf:
        sm_client = MagicMock()
        sm_client.get_secret_value = MagicMock()
        sm_client.get_secret_value.side_effect = Exception
        cf.get_client_for_service.return_value = sm_client
        with pytest.raises(RuntimeError) as e:
            # Act
            _ = get_secret_string(valid_arn)

    # Assert
    assert e.match(regexp=".*Exception.*")
