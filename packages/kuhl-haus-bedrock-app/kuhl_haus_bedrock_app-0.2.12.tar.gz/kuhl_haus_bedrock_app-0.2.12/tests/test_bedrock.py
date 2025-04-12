import json
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from kuhl_haus.bedrock.app.bedrock import (
    BedrockModel,
    BedrockEmbeddingsModel,
    CohereEmbeddingsModel,
    TitanEmbeddingsModel,
    get_embeddings_model,
    get_inference_region_prefix,
    list_bedrock_models
)
from kuhl_haus.bedrock.app.schema import (
    ChatRequest,
    UserMessage,
    TextContent,
    ImageContent,
    Function,
    EmbeddingsRequest
)


# Fixtures for mocking AWS services
@pytest.fixture
def mock_bedrock_runtime():
    with patch('kuhl_haus.bedrock.app.bedrock.bedrock_runtime') as mock:
        yield mock


@pytest.fixture
def mock_bedrock_client():
    with patch('kuhl_haus.bedrock.app.bedrock.bedrock_client') as mock:
        yield mock


@pytest.fixture
def mock_logger():
    with patch('kuhl_haus.bedrock.app.bedrock.logger') as mock:
        yield mock


@pytest.fixture
def mock_requests():
    with patch('kuhl_haus.bedrock.app.bedrock.requests') as mock:
        yield mock


# Tests for utility functions
def test_get_inference_region_prefix_for_ap_regions():
    # Arrange
    with patch('kuhl_haus.bedrock.app.bedrock.AWS_REGION', 'ap-northeast-1'):
        # Act
        result = get_inference_region_prefix()

        # Assert
        assert result == 'apac'


def test_get_inference_region_prefix_for_non_ap_regions():
    # Arrange
    with patch('kuhl_haus.bedrock.app.bedrock.AWS_REGION', 'us-east-1'):
        # Act
        result = get_inference_region_prefix()

        # Assert
        assert result == 'us'


def test_list_bedrock_models_successful(mock_bedrock_client):
    # Arrange
    mock_bedrock_client.list_foundation_models.return_value = {
        'modelSummaries': [
            {
                'modelId': 'model1',
                'responseStreamingSupported': True,
                'modelLifecycle': {'status': 'ACTIVE'},
                'inferenceTypesSupported': ['ON_DEMAND'],
                'inputModalities': ['TEXT']
            }
        ]
    }
    mock_bedrock_client.list_inference_profiles.return_value = {
        'inferenceProfileSummaries': [
            {'inferenceProfileId': 'us.model1'}
        ]
    }

    with patch('kuhl_haus.bedrock.app.bedrock.ENABLE_CROSS_REGION_INFERENCE', True):
        with patch('kuhl_haus.bedrock.app.bedrock.cr_inference_prefix', 'us'):
            # Act
            result = list_bedrock_models()

            # Assert
            assert 'model1' in result
            assert 'us.model1' in result
            assert result['model1']['modalities'] == ['TEXT']


def test_list_bedrock_models_exception(mock_bedrock_client, mock_logger):
    # Arrange
    mock_bedrock_client.list_foundation_models.side_effect = Exception("API error")

    with patch('kuhl_haus.bedrock.app.bedrock.DEFAULT_MODEL', 'default-model'):
        # Act
        result = list_bedrock_models()

        # Assert
        assert 'default-model' in result
        mock_logger.error.assert_called_once()


# Tests for BedrockModel class
def test_list_models_returns_updated_list():
    # Arrange
    with patch('kuhl_haus.bedrock.app.bedrock.list_bedrock_models') as mock_list:
        mock_list.return_value = {'model1': {}, 'model2': {}}
        sut = BedrockModel()

        # Act
        result = sut.list_models()

        # Assert
        assert result == ['model1', 'model2']
        mock_list.assert_called_once()


def test_validate_raises_exception_for_unsupported_model():
    # Arrange
    with patch('kuhl_haus.bedrock.app.bedrock.bedrock_model_list', {'supported-model': {}}):
        sut = BedrockModel()
        request = ChatRequest(model="unsupported-model", messages=[])

        # Act & Assert
        with pytest.raises(HTTPException) as exc_info:
            sut.validate(request)

        assert exc_info.value.status_code == 400
        assert "Unsupported model" in exc_info.value.detail


def test_invoke_bedrock_successful(mock_bedrock_runtime):
    # Arrange
    mock_bedrock_runtime.converse.return_value = {"result": "success"}

    with patch.object(BedrockModel, '_parse_request', return_value={"modelId": "test-model"}):
        sut = BedrockModel()
        request = ChatRequest(model="test-model", messages=[])

        # Act
        result = sut._invoke_bedrock(request)

        # Assert
        assert result == {"result": "success"}
        mock_bedrock_runtime.converse.assert_called_once_with(modelId="test-model")


def test_chat_returns_formatted_response(mock_bedrock_runtime):
    # Arrange
    mock_response = {
        "output": {
            "message": {
                "content": [{"text": "Hello there"}]
            }
        },
        "usage": {
            "inputTokens": 10,
            "outputTokens": 20
        },
        "stopReason": "stop"
    }
    mock_bedrock_runtime.converse.return_value = mock_response

    with patch.object(BedrockModel, '_parse_request'):
        with patch.object(BedrockModel, 'generate_message_id', return_value="msg123"):
            sut = BedrockModel()
            request = ChatRequest(model="test-model", messages=[])

            # Act
            result = sut.chat(request)

            # Assert
            assert result.id == "msg123"
            assert result.model == "test-model"
            assert result.choices[0].message.content == "Hello there"
            assert result.usage.prompt_tokens == 10
            assert result.usage.completion_tokens == 20


def test_parse_system_prompts():
    # Arrange
    sut = BedrockModel()
    request = ChatRequest(
        model="test-model",
        messages=[  # noqa
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": "Hello"}
        ]
    )

    # Act
    result = sut._parse_system_prompts(request)

    # Assert
    assert result == [{"text": "You are a helpful assistant"}]


def test_parse_messages_basic():
    # Arrange
    sut = BedrockModel()
    request = ChatRequest(
        model="test-model",
        messages=[
            UserMessage(role="user", content="Hello")
        ]
    )

    # Act
    result = sut._parse_messages(request)

    # Assert
    assert len(result) == 1
    assert result[0]["role"] == "user"
    assert result[0]["content"][0]["text"] == "Hello"


def test_parse_content_parts_text():
    # Arrange
    sut = BedrockModel()
    message = UserMessage(role="user", content="Hello")

    # Act
    result = sut._parse_content_parts(message, "test-model")

    # Assert
    assert result == [{"text": "Hello"}]


def test_parse_content_parts_multimodal():
    # Arrange
    sut = BedrockModel()
    message = UserMessage(
        role="user",
        content=[
            TextContent(text="Look at this image:"),
            ImageContent(image_url={"url": "data:image/jpeg;base64,SGVsbG8="})  # noqa
        ]
    )

    with patch.object(BedrockModel, 'is_supported_modality', return_value=True):
        # Act
        result = sut._parse_content_parts(message, "test-model")

        # Assert
        assert len(result) == 2
        assert result[0]["text"] == "Look at this image:"
        assert "image" in result[1]
        assert result[1]["image"]["format"] == "jpeg"


def test_is_supported_modality():
    # Arrange
    with patch('kuhl_haus.bedrock.app.bedrock.bedrock_model_list', {
        'model1': {'modalities': ['TEXT', 'IMAGE']},
        'model2': {'modalities': ['TEXT']}
    }):
        sut = BedrockModel()

        # Act
        result1 = sut.is_supported_modality('model1', 'IMAGE')
        result2 = sut.is_supported_modality('model2', 'IMAGE')

        # Assert
        assert result1 is True
        assert result2 is False


def test_convert_tool_spec():
    # Arrange
    sut = BedrockModel()
    function = Function(
        name="get_weather",
        description="Get the weather for a location",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The location to get weather for"
                }
            },
            "required": ["location"]
        }
    )

    # Act
    result = sut._convert_tool_spec(function)

    # Assert
    assert result["toolSpec"]["name"] == "get_weather"
    assert result["toolSpec"]["description"] == "Get the weather for a location"
    assert "json" in result["toolSpec"]["inputSchema"]


def test_calc_budget_tokens():
    # Arrange
    sut = BedrockModel()

    # Act
    low_result = sut._calc_budget_tokens(1000, "low")
    medium_result = sut._calc_budget_tokens(1000, "medium")
    high_result = sut._calc_budget_tokens(1000, "high")

    # Assert
    assert low_result == 300
    assert medium_result == 600
    assert high_result == 999


def test_convert_finish_reason():
    # Arrange
    sut = BedrockModel()

    # Act & Assert
    assert sut._convert_finish_reason("tool_use") == "tool_calls"
    assert sut._convert_finish_reason("finished") == "stop"
    assert sut._convert_finish_reason("max_tokens") == "length"
    assert sut._convert_finish_reason("content_filtered") == "content_filter"
    assert sut._convert_finish_reason("unknown") == "unknown"
    assert sut._convert_finish_reason(None) is None


# Tests for embedding models
def test_get_embeddings_model_cohere():
    # Arrange & Act
    with patch('kuhl_haus.bedrock.app.bedrock.SUPPORTED_BEDROCK_EMBEDDING_MODELS', {
        'cohere.embed-english-v3': 'Cohere Embed English'
    }):
        model = get_embeddings_model('cohere.embed-english-v3')

    # Assert
    assert isinstance(model, CohereEmbeddingsModel)


def test_get_embeddings_model_unsupported():
    # Arrange & Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        get_embeddings_model('unsupported-model')

    assert exc_info.value.status_code == 400
    assert "Unsupported embedding model" in exc_info.value.detail


def test_cohere_parse_args_string_input():
    # Arrange
    sut = CohereEmbeddingsModel()
    request = EmbeddingsRequest(model="cohere.embed-english-v3", input="Test text")

    # Act
    result = sut._parse_args(request)

    # Assert
    assert result["texts"] == ["Test text"]
    assert result["input_type"] == "search_document"
    assert result["truncate"] == "END"


def test_cohere_parse_args_list_input():
    # Arrange
    sut = CohereEmbeddingsModel()
    request = EmbeddingsRequest(model="cohere.embed-english-v3", input=["Text 1", "Text 2"])

    # Act
    result = sut._parse_args(request)

    # Assert
    assert result["texts"] == ["Text 1", "Text 2"]


def test_cohere_embed(mock_bedrock_runtime):
    # Arrange
    mock_response = MagicMock()
    mock_response.get.return_value.read.return_value = json.dumps({
        "embeddings": [[0.1, 0.2, 0.3]]
    })
    mock_bedrock_runtime.invoke_model.return_value = mock_response

    sut = CohereEmbeddingsModel()
    request = EmbeddingsRequest(model="cohere.embed-english-v3", input="Test text")

    with patch.object(CohereEmbeddingsModel, '_parse_args', return_value={"texts": ["Test text"]}):
        # Act
        result = sut.embed(request)

        # Assert
        assert result.model == "cohere.embed-english-v3"
        assert len(result.data) == 1
        assert result.data[0].embedding == [0.1, 0.2, 0.3]
        mock_bedrock_runtime.invoke_model.assert_called_once()


def test_titan_parse_args_string_input():
    # Arrange
    sut = TitanEmbeddingsModel()
    request = EmbeddingsRequest(model="amazon.titan-embed-text-v1", input="Test text")

    # Act
    result = sut._parse_args(request)

    # Assert
    assert result["inputText"] == "Test text"


def test_titan_parse_args_list_input():
    # Arrange
    sut = TitanEmbeddingsModel()
    request = EmbeddingsRequest(model="amazon.titan-embed-text-v1", input=["Test text"])

    # Act
    result = sut._parse_args(request)

    # Assert
    assert result["inputText"] == "Test text"


def test_titan_parse_args_invalid_input():
    # Arrange
    sut = TitanEmbeddingsModel()
    request = EmbeddingsRequest(model="amazon.titan-embed-text-v1", input=["Text 1", "Text 2"])

    # Act & Assert
    with pytest.raises(ValueError) as exc_info:
        sut._parse_args(request)

    assert "support only single strings" in str(exc_info.value)


def test_titan_embed(mock_bedrock_runtime):
    # Arrange
    mock_response = MagicMock()
    mock_response.get.return_value.read.return_value = json.dumps({
        "embedding": [0.1, 0.2, 0.3],
        "inputTextTokenCount": 5
    })
    mock_bedrock_runtime.invoke_model.return_value = mock_response

    sut = TitanEmbeddingsModel()
    request = EmbeddingsRequest(model="amazon.titan-embed-text-v1", input="Test text")

    with patch.object(TitanEmbeddingsModel, '_parse_args', return_value={"inputText": "Test text"}):
        # Act
        result = sut.embed(request)

        # Assert
        assert result.model == "amazon.titan-embed-text-v1"
        assert len(result.data) == 1
        assert result.data[0].embedding == [0.1, 0.2, 0.3]
        assert result.usage.prompt_tokens == 5
        mock_bedrock_runtime.invoke_model.assert_called_once()


def test_embedding_model_create_response_base64():
    # Arrange
    class TestEmbeddingsModel(BedrockEmbeddingsModel):
        def embed(self, request): pass

    sut = TestEmbeddingsModel()
    embeddings = [[0.1, 0.2, 0.3]]

    # Act
    result = sut._create_response(
        embeddings=embeddings,  # noqa
        model="test-model",
        input_tokens=10,
        output_tokens=0,
        encoding_format="base64"
    )

    # Assert
    assert result.model == "test-model"
    assert result.usage.prompt_tokens == 10
    assert len(result.data) == 1
    # The embedding should be base64 encoded
    assert isinstance(result.data[0].embedding, bytes)
