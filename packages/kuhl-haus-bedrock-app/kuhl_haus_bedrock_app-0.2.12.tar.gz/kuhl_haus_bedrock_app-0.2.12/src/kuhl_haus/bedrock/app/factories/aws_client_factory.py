from boto3.session import Session
from botocore.config import Config

from kuhl_haus.bedrock.app.env import (
    AWS_REGION,
    AWS_SIG_VERSION,
    BOTO3_BACKOFF_ON_EXCEPTION_MAX_TRIES,
    BOTO3_BACKOFF_ON_EXCEPTION_MODE,
)


# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html#overview
def __get_default_config() -> Config:
    return Config(
        region_name=AWS_REGION,
        signature_version=AWS_SIG_VERSION,
        retries={
            "max_attempts": BOTO3_BACKOFF_ON_EXCEPTION_MAX_TRIES,
            "mode": BOTO3_BACKOFF_ON_EXCEPTION_MODE,
        },
    )


def __get_default_session() -> Session:
    return Session(region_name=AWS_REGION)


def get_client_for_service(service_name, session: Session = None, config: Config = None):
    """
    This method will return a boto3 client for the service_name given.

    :param service_name: Valid name of an AWS service
    :param session: Optional - boto3 session
    :param config: Optional- boto3 config
    """
    if session is None:
        session = __get_default_session()
    if config is None:
        config = __get_default_config()
    available_services = session.get_available_services()
    if service_name in available_services:
        return session.client(service_name=service_name, config=config)
    raise ValueError("Requested service name ({}) is not available.".format(service_name))


def get_resource_for_service(service_name, session: Session = None, config: Config = None):
    """
    This method will return a boto3 resource for the service_name given.

    :param service_name: Valid name of an AWS service
    :param session: Optional - boto3 session
    :param config: Optional - boto3 config
    """

    if session is None:
        session = __get_default_session()
    if config is None:
        config = __get_default_config()
    available_resources = session.get_available_resources()
    if service_name in available_resources:
        return session.resource(service_name=service_name, config=config)
    raise ValueError("Requested service name ({}) is not available.".format(service_name))
