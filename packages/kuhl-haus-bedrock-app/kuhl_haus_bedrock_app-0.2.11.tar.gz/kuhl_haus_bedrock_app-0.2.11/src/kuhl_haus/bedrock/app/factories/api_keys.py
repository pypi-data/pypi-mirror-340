from kuhl_haus.bedrock.app.api_keys.default_key_auth import DefaultKeyAuth
from kuhl_haus.bedrock.app.api_keys.aws_secret_auth import AwsSecretAuth


def get_api_key_validator():
    asa = AwsSecretAuth()
    if asa.is_valid():
        return asa

    dka = DefaultKeyAuth()
    if dka.is_valid():
        return dka

    raise RuntimeError("No valid API key found")
