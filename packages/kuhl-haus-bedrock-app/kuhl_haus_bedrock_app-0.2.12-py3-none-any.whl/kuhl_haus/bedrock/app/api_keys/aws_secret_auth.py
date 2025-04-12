from typing import Union

from kuhl_haus.bedrock.app.api_keys.api_key_auth import ApiKeyAuth
from kuhl_haus.bedrock.app.helpers.parameter_store_helper import get_ssm_parameter
from kuhl_haus.bedrock.app.helpers.secrets_manager_helper import get_secret_string
from kuhl_haus.bedrock.app.env import SECRET_ARN_PARAMETER


class AwsSecretAuth(ApiKeyAuth):
    api_key_secret_arn: Union[str, None]

    def __init__(self):
        if SECRET_ARN_PARAMETER:
            self.api_key_secret_arn = get_ssm_parameter(parameter_name=SECRET_ARN_PARAMETER)
            api_key = get_secret_string(arn=self.api_key_secret_arn)
        else:
            self.api_key_secret_arn = None
            api_key = None
        super().__init__(api_key=api_key)

    def is_valid(self) -> bool:
        return bool(self.api_key_secret_arn)
