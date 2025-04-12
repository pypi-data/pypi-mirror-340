from unittest.mock import MagicMock, create_autospec, patch

import pytest
from boto3.resources.base import ServiceResource
from boto3.session import Config, Session

from kuhl_haus.bedrock.app.factories.aws_client_factory import (
    get_client_for_service,
    get_resource_for_service,
)


class MockBotoClient(MagicMock):
    pass


@pytest.fixture()
def mock_boto_client_session():
    # Session - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html
    session = create_autospec(Session)
    # Client -
    session.client = MockBotoClient()
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.get_available_services  # noqa
    session.get_available_services = MagicMock()
    return session


@pytest.fixture()
def mock_boto_resource_session():
    # Session - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html
    session = create_autospec(Session)
    # Resources - https://boto3.amazonaws.com/v1/documentation/api/latest/guide/resources.html
    session.resource = create_autospec(ServiceResource)
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html#boto3.session.Session.get_available_resources  # noqa
    session.get_available_resources = MagicMock()
    return session


@pytest.fixture()
def valid_service_name():
    return "valid_service_name"


@pytest.fixture()
def invalid_service_name():
    return "invalid_service_name"


@pytest.fixture()
def mock_available_services(valid_service_name):
    return [valid_service_name]


@pytest.fixture()
def mock_available_resources(valid_service_name):
    return [valid_service_name]


def test_get_resource_for_service_happy_path_with_provided_session_expect_resource_instance(
    mock_boto_resource_session,
    valid_service_name,
    mock_available_resources,
):
    """
    This test is intended to test the happy path when a Session is provided to the factory method.

    :param mock_boto_resource_session: Pytest fixture - passed to sut as existing Session
    :param valid_service_name: Pytest fixture
    :param mock_available_resources: Pytest fixture
    """

    # Arrange
    sut = get_resource_for_service
    mock_boto_resource_session.get_available_resources.return_value = mock_available_resources

    # Act
    result = sut(service_name=valid_service_name, session=mock_boto_resource_session)

    # Assert
    assert isinstance(result, ServiceResource)


@patch("kuhl_haus.bedrock.app.factories.aws_client_factory.Session")
def test_get_resource_for_service_happy_path_with_defaults_expect_resource_instance(
    boto_session,
    mock_boto_resource_session,
    valid_service_name,
    mock_available_resources,
):
    """
    This test is intended to test the happy path using the default Session.

    :param boto_session: Patched boto3.session call
    :param mock_boto_resource_session: Pytest fixture
    :param valid_service_name: Pytest fixture
    :param mock_available_resources: Pytest fixture
    """

    # Arrange
    sut = get_resource_for_service
    mock_boto_resource_session.get_available_resources.return_value = mock_available_resources
    boto_session.return_value = mock_boto_resource_session

    # Act
    result = sut(service_name=valid_service_name, session=None)

    # Assert
    assert isinstance(result, ServiceResource)


@patch("kuhl_haus.bedrock.app.factories.aws_client_factory.Session")
def test_get_resource_for_service_with_invalid_service_name_expect_value_error_exception(
    boto_session,
    mock_boto_resource_session,
    invalid_service_name,
    mock_available_resources,
):
    """
    This test ensures that a ValueError is raised when an invalid service name is passed.

    :param boto_session: Patched boto3.session call
    :param mock_boto_resource_session: Pytest fixture
    :param invalid_service_name: Pytest fixture
    :param mock_available_resources: Pytest fixture
    """

    # Arrange
    sut = get_resource_for_service
    mock_boto_resource_session.get_available_resources.return_value = mock_available_resources

    with pytest.raises(ValueError) as e:
        # Act
        _ = sut(service_name=invalid_service_name, session=mock_boto_resource_session)

        # Assert
        assert invalid_service_name in repr(e)


def test_get_client_for_service_happy_path_with_provided_session_expect_client_instance(
    mock_boto_client_session,
    valid_service_name,
    mock_available_services,
):
    """
    This test is intended to test the happy path when a Session is provided to the factory method.

    :param mock_boto_client_session: Pytest fixture - passed to sut as existing Session
    :param valid_service_name: Pytest fixture
    :param mock_available_services: Pytest fixture
    """

    # Arrange
    sut = get_client_for_service
    mock_boto_client_session.get_available_services.return_value = mock_available_services

    # Act
    result = sut(service_name=valid_service_name, session=mock_boto_client_session)

    # Assert
    assert isinstance(result, MockBotoClient)


def test_get_client_for_service_happy_path_with_provided_config_expect_client_instance(
    mock_boto_client_session,
    valid_service_name,
    mock_available_services,
):
    """
    This test is intended to test the happy path when a Config is provided to the factory method.

    :param mock_boto_client_session: Pytest fixture - passed to sut as existing Session
    :param valid_service_name: Pytest fixture
    :param mock_available_services: Pytest fixture
    """

    # Arrange
    mock_config = create_autospec(Config)
    sut = get_client_for_service
    mock_boto_client_session.get_available_services.return_value = mock_available_services

    # Act
    result = sut(
        service_name=valid_service_name, session=mock_boto_client_session, config=mock_config
    )

    # Assert
    assert isinstance(result, MockBotoClient)


def test_get_resource_for_service_happy_path_with_provided_config_expect_resource_instance(
    mock_boto_resource_session,
    valid_service_name,
    mock_available_resources,
):
    """
    This test is intended to test the happy path when a Config is provided to the factory method.

    :param mock_boto_resource_session: Pytest fixture - passed to sut as existing Session
    :param valid_service_name: Pytest fixture
    :param mock_available_resources: Pytest fixture
    """

    # Arrange
    mock_config = create_autospec(Config)
    sut = get_resource_for_service
    mock_boto_resource_session.get_available_resources.return_value = mock_available_resources

    # Act
    result = sut(
        service_name=valid_service_name, session=mock_boto_resource_session, config=mock_config
    )

    # Assert
    assert isinstance(result, ServiceResource)


@patch("kuhl_haus.bedrock.app.factories.aws_client_factory.Session")
def test_get_client_for_service_happy_path_with_defaults_expect_client_instance(
    boto_session,
    mock_boto_client_session,
    valid_service_name,
    mock_available_services,
):
    """
    This test is intended to test the happy path using the default Session.

    :param mock_boto_client_session: Pytest fixture - passed to sut as existing Session
    :param valid_service_name: Pytest fixture
    :param mock_available_services: Pytest fixture
    """

    # Arrange
    sut = get_client_for_service
    mock_boto_client_session.get_available_services.return_value = mock_available_services
    boto_session.return_value = mock_boto_client_session

    # Act
    result = sut(service_name=valid_service_name, session=None)

    # Assert
    assert isinstance(result, MockBotoClient)


@patch("kuhl_haus.bedrock.app.factories.aws_client_factory.Session")
def test_get_client_for_service_with_invalid_service_name_expect_value_error_exception(
    boto_session,
    mock_boto_client_session,
    invalid_service_name,
    mock_available_services,
):
    """
    This test ensures that a ValueError is raised when an invalid service name is passed.

    :param boto_session: Patched boto3.session call
    :param mock_boto_client_session: Pytest fixture
    :param invalid_service_name: Pytest fixture
    :param mock_available_services: Pytest fixture
    """

    # Arrange
    sut = get_client_for_service
    mock_boto_client_session.get_available_services.return_value = mock_available_services
    boto_session.return_value = mock_boto_client_session

    with pytest.raises(ValueError) as e:
        # Act
        _ = sut(service_name=invalid_service_name, session=None)

        # Assert
        assert invalid_service_name in repr(e)
