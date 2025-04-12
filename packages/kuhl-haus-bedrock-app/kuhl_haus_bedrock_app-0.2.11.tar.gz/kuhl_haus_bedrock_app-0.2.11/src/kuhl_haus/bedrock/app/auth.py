from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from kuhl_haus.bedrock.app.env import SECRET_ARN_PARAMETER
from kuhl_haus.bedrock.app.helpers.parameter_store_helper import get_ssm_parameter
from kuhl_haus.bedrock.app.helpers.secrets_manager_helper import get_secret_string

api_key_secret_arn = get_ssm_parameter(parameter_name=SECRET_ARN_PARAMETER)
api_key = get_secret_string(arn=api_key_secret_arn)

security = HTTPBearer()


def api_key_auth(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
):
    if credentials.credentials != api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API Key")
