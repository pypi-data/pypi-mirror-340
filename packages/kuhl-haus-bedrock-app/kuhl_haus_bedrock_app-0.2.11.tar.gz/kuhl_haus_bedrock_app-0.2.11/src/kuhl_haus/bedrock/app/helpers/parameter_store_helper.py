from __future__ import annotations

from functools import lru_cache

from kuhl_haus.bedrock.app.factories import aws_client_factory


@lru_cache()
def get_ssm_parameter(parameter_name):
    try:
        client = aws_client_factory.get_client_for_service("ssm")
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ssm/client/get_parameter.html
        response = client.get_parameter(Name=parameter_name, WithDecryption=True)

        if "Parameter" in response:
            return response["Parameter"]["Value"]
        else:
            raise RuntimeError(f"Parameter not found in response: {response}")
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"Unhandled exception raised: {repr(e)}") from e
