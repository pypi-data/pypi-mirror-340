from kuhl_haus.bedrock.app.api_keys.api_key_auth import ApiKeyAuth
from kuhl_haus.bedrock.app.env import DEFAULT_API_KEY


class DefaultKeyAuth(ApiKeyAuth):
    def __init__(self):
        super().__init__(api_key=DEFAULT_API_KEY)

    def is_valid(self) -> bool:
        return bool(self.api_key)
