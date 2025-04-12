import os

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

# AWS Client
AWS_REGION = os.environ.get("AWS_REGION", "us-west-2")
AWS_SIG_VERSION = os.environ.get("AWS_SIG_VERSION", "v4")
# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/retries.html#standard-retry-mode
BOTO3_BACKOFF_ON_EXCEPTION_MODE = os.environ.get("BOTO3_BACKOFF_ON_EXCEPTION_MODE", "standard")
BOTO3_BACKOFF_ON_EXCEPTION_MAX_TRIES = os.environ.get("BOTO3_BACKOFF_ON_EXCEPTION_MAX_TRIES", 3)

# API Settings
DEFAULT_API_KEY = os.environ.get("DEFAULT_API_KEY")
SECRET_ARN_PARAMETER = os.environ.get("SECRET_ARN_PARAMETER")
DEFAULT_MODEL = os.environ.get(
    "DEFAULT_MODEL", "anthropic.claude-3-5-haiku-20241022-v1:0"
)
DEFAULT_EMBEDDING_MODEL = os.environ.get(
    "DEFAULT_EMBEDDING_MODEL", "cohere.embed-multilingual-v3"
)
ENABLE_CROSS_REGION_INFERENCE = os.environ.get("ENABLE_CROSS_REGION_INFERENCE", "true").lower() != "false"
