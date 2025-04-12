from __future__ import annotations

from functools import lru_cache

from kuhl_haus.bedrock.app.factories import aws_client_factory


@lru_cache()
def get_secret_string(arn):
    try:
        client = aws_client_factory.get_client_for_service("secretsmanager")
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_secret_value.html
        response = client.get_secret_value(SecretId=arn)

        if "SecretString" in response:
            return response["SecretString"]
        else:
            raise RuntimeError(f"SecretString not found in response: {response}")
    except RuntimeError:
        raise
    except Exception as e:
        raise RuntimeError(f"Unhandled exception raised: {repr(e)}") from e
