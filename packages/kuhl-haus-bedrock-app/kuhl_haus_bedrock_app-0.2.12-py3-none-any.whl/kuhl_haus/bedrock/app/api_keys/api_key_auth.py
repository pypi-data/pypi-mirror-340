from abc import ABC, abstractmethod
from typing import Union
from fastapi.security import HTTPAuthorizationCredentials


class ApiKeyAuth(ABC):
    api_key: Union[str, None]

    def __init__(self, api_key=None):
        self.api_key = api_key

    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError("Subclasses must implement this method")

    def validate_credentials(self, credentials: HTTPAuthorizationCredentials) -> bool:
        return bool(credentials.credentials == self.api_key)
