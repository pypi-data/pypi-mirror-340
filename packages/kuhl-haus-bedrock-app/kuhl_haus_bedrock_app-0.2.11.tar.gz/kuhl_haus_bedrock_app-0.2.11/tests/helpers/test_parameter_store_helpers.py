import uuid
from datetime import datetime
from random import choice
from unittest.mock import MagicMock, patch

import pytest

from kuhl_haus.bedrock.app.helpers.parameter_store_helper import get_ssm_parameter


def get_pseudorandom_name():
    # Generate a fake ARN from a UUID so lru_cache doesn't skew results
    choices_string = uuid.uuid4().hex
    arn = ""
    for x in range(0, 12):
        arn = arn + choice(choices_string)
    return arn


@pytest.fixture()
def valid_name():
    return get_pseudorandom_name()


@pytest.fixture()
def valid_value():
    return "valid_value"


def valid_get_parameter_response(name: str, value: str):
    return {
        "Parameter": {
            "Name": name,
            "Type": "String",
            "Value": value,
            "Version": 1,
            "Selector": "string",
            "SourceResult": "string",
            "LastModifiedDate": datetime(2015, 1, 1),
            "ARN": f"arn:fake:{name}",
            "DataType": "string",
        }
    }


def mock_ssm_client(name, value):
    mock = MagicMock()
    mock.get_parameter = MagicMock()
    mock.get_parameter.return_value = valid_get_parameter_response(name, value)
    return mock


def test_get_ssm_parameter_happy_path(valid_name, valid_value):
    # Arrange
    with patch("kuhl_haus.bedrock.app.helpers.parameter_store_helper.aws_client_factory") as cf:
        cf.get_client_for_service.return_value = mock_ssm_client(valid_name, valid_value)
        sut = get_ssm_parameter

        # Act
        result = sut(valid_name)

    # Assert
    assert valid_value == result


def test_get_ssm_parameter_with_positive_cache_hit_happy_path(valid_name, valid_value):
    # Arrange
    with patch("kuhl_haus.bedrock.app.helpers.parameter_store_helper.aws_client_factory") as cf:
        cf.get_client_for_service.return_value = mock_ssm_client(valid_name, valid_value)
        sut = get_ssm_parameter

        # Act
        cache_info_0 = sut.cache_info()
        print(cache_info_0)

        result1 = sut(valid_name)
        cache_info_1 = sut.cache_info()
        print(cache_info_1)

        result2 = sut(valid_name)
        cache_info_2 = sut.cache_info()
        print(cache_info_2)

    # Assert
    assert valid_value == result1
    assert valid_value == result2
    # CacheInfo is a tuple:
    # hits, misses, max_size, current_size = cache_info_n
    assert cache_info_0[3] < cache_info_1[3]  # assert cache size increased
    assert cache_info_1[3] == cache_info_2[3]  # assert cache size did not increase
    assert cache_info_2[0] > cache_info_1[0]  # assert hits increased
    assert cache_info_2[1] == cache_info_1[1]  # assert misses did not increase


def test_get_ssm_parameter_with_negative_cache_hit_happy_path(valid_name, valid_value):
    # Arrange
    with patch("kuhl_haus.bedrock.app.helpers.parameter_store_helper.aws_client_factory") as cf:
        cf.get_client_for_service.return_value = mock_ssm_client(valid_name, valid_value)
        sut = get_ssm_parameter

        # Act
        cache_info_0 = sut.cache_info()
        print(cache_info_0)

        result1 = sut(valid_name)
        cache_info_1 = sut.cache_info()
        print(cache_info_1)

        result2 = sut(get_pseudorandom_name())
        cache_info_2 = sut.cache_info()
        print(cache_info_2)

    # Assert
    assert valid_value == result1
    assert valid_value == result2
    # CacheInfo is a tuple:
    # hits, misses, max_size, current_size = cache_info_n
    assert cache_info_0[3] < cache_info_1[3]  # assert cache size increased
    assert cache_info_1[3] < cache_info_2[3]  # assert cache size increased
    assert cache_info_2[0] == cache_info_1[0]  # assert hits did not increase
    assert cache_info_2[1] > cache_info_1[1]  # assert misses increased


def test_get_ssm_parameter_with_empty_response_expect_runtime_error(valid_name, valid_value):
    # Arrange
    with patch("kuhl_haus.bedrock.app.helpers.parameter_store_helper.aws_client_factory") as cf:
        ssm_client = MagicMock()
        ssm_client.get_parameter = MagicMock()
        ssm_client.get_parameter.return_value = {}
        cf.get_client_for_service.return_value = ssm_client
        with pytest.raises(RuntimeError) as e:
            # Act
            _ = get_ssm_parameter(valid_name)

    # Assert
    assert e.match(regexp=".*Parameter.*")


def test_get_ssm_parameter_with_unhandled_exception_expect_runtime_error(valid_name, valid_value):
    # Arrange
    with patch("kuhl_haus.bedrock.app.helpers.parameter_store_helper.aws_client_factory") as cf:
        ssm_client = MagicMock()
        ssm_client.get_parameter = MagicMock()
        ssm_client.get_parameter.side_effect = Exception
        cf.get_client_for_service.return_value = ssm_client
        with pytest.raises(RuntimeError) as e:
            # Act
            _ = get_ssm_parameter(valid_name)

    # Assert
    assert e.match(regexp=".*Exception.*")
