from unittest.mock import patch, MagicMock

import pytest

from kuhl_haus.bedrock.app.bedrock import (
    BedrockModel,
    CohereEmbeddingsModel,
    get_inference_region_prefix,
    list_bedrock_models,
    get_embeddings_model
)
from kuhl_haus.bedrock.app.schema import (
    ChatRequest,
    ChatResponse,
    UserMessage,
    EmbeddingsRequest
)


@pytest.fixture
def mock_bedrock_runtime():
    return MagicMock()


@pytest.fixture
def mock_bedrock_client():
    return MagicMock()


@patch('kuhl_haus.bedrock.app.bedrock.AWS_REGION', 'us-east-1')
def test_get_inference_region_prefix_us_region():
    """Test get_inference_region_prefix with US region."""
    # Arrange

    # Act
    result = get_inference_region_prefix()

    # Assert
    assert result == 'us'


@patch('kuhl_haus.bedrock.app.bedrock.AWS_REGION', 'ap-southeast-1')
def test_get_inference_region_prefix_ap_region():
    """Test get_inference_region_prefix with APAC region."""
    # Arrange

    # Act
    result = get_inference_region_prefix()

    # Assert
    assert result == 'apac'


@patch('kuhl_haus.bedrock.app.bedrock.bedrock_client')
@patch('kuhl_haus.bedrock.app.bedrock.ENABLE_CROSS_REGION_INFERENCE', True)
def test_list_bedrock_models_with_cross_region(patched_bedrock_client):
    """Test list_bedrock_models with cross-region inference enabled."""
    # Arrange
    patched_bedrock_client.list_inference_profiles.return_value = {
        'inferenceProfileSummaries': [
            {'inferenceProfileId': 'us.anthropic.claude-3-sonnet-20240229-v1:0'}
        ]
    }

    patched_bedrock_client.list_foundation_models.return_value = {
        'modelSummaries': [
            {
                'modelId': 'anthropic.claude-3-sonnet-20240229-v1:0',
                'responseStreamingSupported': True,
                'modelLifecycle': {'status': 'ACTIVE'},
                'inferenceTypesSupported': ['ON_DEMAND'],
                'inputModalities': ['TEXT', 'IMAGE']
            }
        ]
    }

    # Act
    result = list_bedrock_models()

    # Assert
    assert 'anthropic.claude-3-sonnet-20240229-v1:0' in result
    assert result['anthropic.claude-3-sonnet-20240229-v1:0']['modalities'] == ['TEXT', 'IMAGE']

    # Cross-region model should be included
    assert 'us.anthropic.claude-3-sonnet-20240229-v1:0' in result


@patch('kuhl_haus.bedrock.app.bedrock.bedrock_client')
def test_list_bedrock_models_handles_exception(patched_bedrock_client):
    """Test list_bedrock_models handles exceptions gracefully."""
    # Arrange
    patched_bedrock_client.list_foundation_models.side_effect = Exception("API Error")

    # Act
    result = list_bedrock_models()

    # Assert
    assert isinstance(result, dict)
    # Should include DEFAULT_MODEL as fallback
    assert len(result) > 0


@patch('kuhl_haus.bedrock.app.bedrock.bedrock_model_list', {
    'anthropic.claude-3-sonnet-20240229-v1:0': {'modalities': ['TEXT']}
})
def test_bedrock_model_list_models():
    """Test BedrockModel.list_models returns the current model list."""
    # Arrange
    sut = BedrockModel()

    # Act
    with patch('kuhl_haus.bedrock.app.bedrock.list_bedrock_models') as mock_list_models:
        mock_list_models.return_value = {
            'anthropic.claude-3-sonnet-20240229-v1:0': {'modalities': ['TEXT']},
            'new-model': {'modalities': ['TEXT']}
        }
        result = sut.list_models()

    # Assert
    assert len(result) == 2
    assert 'anthropic.claude-3-sonnet-20240229-v1:0' in result
    assert 'new-model' in result


@patch('kuhl_haus.bedrock.app.bedrock.bedrock_model_list', {
    'valid-model': {'modalities': ['TEXT']}
})
def test_bedrock_model_validate_valid_model():
    """Test BedrockModel.validate with valid model."""
    # Arrange
    sut = BedrockModel()
    request = ChatRequest(model="valid-model", messages=[UserMessage(content="Hello")])

    # Act & Assert
    # Should not raise exception
    sut.validate(request)


@patch('kuhl_haus.bedrock.app.bedrock.bedrock_model_list', {
    'valid-model': {'modalities': ['TEXT']}
})
def test_bedrock_model_validate_invalid_model():
    """Test BedrockModel.validate with invalid model."""
    # Arrange
    from fastapi import HTTPException

    sut = BedrockModel()
    request = ChatRequest(model="invalid-model", messages=[UserMessage(content="Hello")])

    # Act & Assert
    with pytest.raises(HTTPException) as excinfo:
        sut.validate(request)

    assert excinfo.value.status_code == 400
    assert "Unsupported model" in excinfo.value.detail


@patch('kuhl_haus.bedrock.app.bedrock.bedrock_runtime')
@patch('kuhl_haus.bedrock.app.bedrock.bedrock_model_list', {
    'anthropic.claude-3-sonnet-20240229-v1:0': {'modalities': ['TEXT']}
})
def test_bedrock_model_invoke_bedrock(patched_bedrock_runtime):
    """Test BedrockModel._invoke_bedrock normal operation."""
    # Arrange
    sut = BedrockModel()
    request = ChatRequest(
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[UserMessage(content="Hello")]
    )

    patched_bedrock_runtime.converse.return_value = {
        "output": {"message": {"content": "Response text"}},
        "usage": {"inputTokens": 10, "outputTokens": 20},
        "stopReason": "COMPLETE"
    }

    with patch.object(sut, '_parse_request',
                      return_value={"modelId": "anthropic.claude-3-sonnet-20240229-v1:0", "messages": []}):
        # Act
        result = sut._invoke_bedrock(request)

        # Assert
        assert result == patched_bedrock_runtime.converse.return_value
        patched_bedrock_runtime.converse.assert_called_once()


@patch('kuhl_haus.bedrock.app.bedrock.bedrock_runtime')
@patch('kuhl_haus.bedrock.app.bedrock.bedrock_model_list', {
    'anthropic.claude-3-sonnet-20240229-v1:0': {'modalities': ['TEXT']}
})
def test_bedrock_model_invoke_bedrock_with_stream(patched_bedrock_runtime):
    """Test BedrockModel._invoke_bedrock with streaming."""
    # Arrange
    sut = BedrockModel()
    request = ChatRequest(
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[UserMessage(content="Hello")]
    )

    patched_bedrock_runtime.converse_stream.return_value = {
        "stream": [{"chunk": "data"}]
    }

    with patch.object(sut, '_parse_request',
                      return_value={"modelId": "anthropic.claude-3-sonnet-20240229-v1:0", "messages": []}):
        # Act
        result = sut._invoke_bedrock(request, stream=True)

        # Assert
        assert result == patched_bedrock_runtime.converse_stream.return_value
        patched_bedrock_runtime.converse_stream.assert_called_once()


@patch('kuhl_haus.bedrock.app.bedrock.bedrock_runtime')
@patch('kuhl_haus.bedrock.app.bedrock.bedrock_model_list', {
    'anthropic.claude-3-sonnet-20240229-v1:0': {'modalities': ['TEXT']}
})
def test_bedrock_model_invoke_bedrock_validation_error(patched_bedrock_runtime):
    """Test BedrockModel._invoke_bedrock handles validation errors."""
    # Arrange
    from fastapi import HTTPException

    sut = BedrockModel()
    request = ChatRequest(
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[UserMessage(content="Hello")]
    )

    # Create ValidationException mock
    validation_error = type('ValidationException', (Exception,), {})()
    patched_bedrock_runtime.exceptions.ValidationException = validation_error.__class__
    patched_bedrock_runtime.converse.side_effect = validation_error

    with patch.object(sut, '_parse_request',
                      return_value={"modelId": "anthropic.claude-3-sonnet-20240229-v1:0", "messages": []}):
        # Act & Assert
        with pytest.raises(HTTPException) as excinfo:
            sut._invoke_bedrock(request)

        assert excinfo.value.status_code == 400


@patch('kuhl_haus.bedrock.app.bedrock.bedrock_runtime')
def test_bedrock_model_chat(patched_bedrock_runtime):
    """Test BedrockModel.chat normal operation."""
    # Arrange
    sut = BedrockModel()
    request = ChatRequest(
        model="anthropic.claude-3-sonnet-20240229-v1:0",
        messages=[UserMessage(content="Hello")]
    )

    patched_bedrock_runtime.converse.return_value = {
        "output": {"message": {"content": "Response text"}},
        "usage": {"inputTokens": 10, "outputTokens": 20},
        "stopReason": "COMPLETE"
    }

    with patch.object(sut, '_invoke_bedrock', return_value=patched_bedrock_runtime.converse.return_value), \
            patch.object(sut, '_create_response') as mock_create_response, \
            patch.object(sut, 'generate_message_id', return_value="msg_123"):
        mock_create_response.return_value = ChatResponse(
            id="msg_123",
            model="anthropic.claude-3-sonnet-20240229-v1:0",
            choices=[{  # noqa
                "index": 0,
                "message": {"role": "assistant", "content": "Response text"},
                "finish_reason": "stop"
            }],
            usage={"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}  # noqa
        )

        # Act
        result = sut.chat(request)

        # Assert
        assert result.id == "msg_123"
        assert result.model == "anthropic.claude-3-sonnet-20240229-v1:0"
        mock_create_response.assert_called_once_with(
            model="anthropic.claude-3-sonnet-20240229-v1:0",
            message_id="msg_123",
            content="Response text",
            finish_reason="COMPLETE",
            input_tokens=10,
            output_tokens=20
        )


@patch('kuhl_haus.bedrock.app.bedrock.SUPPORTED_BEDROCK_EMBEDDING_MODELS', {
    'cohere.embed-english-v3': 'Cohere Embed English',
    'amazon.titan-embed-text-v1': 'Titan Embeddings G1 - Text'
})
def test_get_embeddings_model_cohere():
    """Test get_embeddings_model returns correct model for Cohere."""
    # Arrange
    model_id = "cohere.embed-english-v3"

    # Act
    result = get_embeddings_model(model_id)

    # Assert
    assert isinstance(result, CohereEmbeddingsModel)


def test_cohereembeddings_model_parse_args():
    """Test CohereEmbeddingsModel._parse_args."""
    # Arrange
    sut = CohereEmbeddingsModel()
    request = EmbeddingsRequest(
        model="cohere.embed-english-v3",
        input=["Hello", "World"]
    )

    # Act
    result = sut._parse_args(request)

    # Assert
    assert "texts" in result
    assert result["texts"] == ["Hello", "World"]
    assert "input_type" in result
