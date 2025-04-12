import traceback
import sys
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from kuhl_haus.bedrock.app.factories.api_keys import get_api_key_validator

key_validator = get_api_key_validator()

security = HTTPBearer()


def api_key_auth(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],):
    try:
        credentials_are_valid = key_validator.validate_credentials(credentials)
        if credentials_are_valid:
            return
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stderr)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Validation error")
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
