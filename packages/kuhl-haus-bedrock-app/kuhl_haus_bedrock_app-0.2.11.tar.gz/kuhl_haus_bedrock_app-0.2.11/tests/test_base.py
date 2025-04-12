import json
import uuid
from typing import AsyncIterable
from unittest.mock import Mock, patch

import pytest

from kuhl_haus.bedrock.app.base import BaseChatModel, BaseEmbeddingsModel
from kuhl_haus.bedrock.app.schema import (
    ChatResponse,
    ChatRequest,
    ChatStreamResponse,
    EmbeddingsRequest,
    EmbeddingsResponse,
)


class ConcreteChatModel(BaseChatModel):
    """Concrete implementation of BaseChatModel for testing purposes."""

    def chat(self, chat_request: ChatRequest) -> ChatResponse:
        return ChatResponse(
            choices=[],
            id="test-id",
            created=123,
            model="test-model",
            usage={  # noqa
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
        )

    def chat_stream(self, chat_request: ChatRequest) -> AsyncIterable[bytes]:
        async def _stream():
            yield b"test stream data"

        return _stream()


class ConcreteEmbeddingsModel(BaseEmbeddingsModel):
    """Concrete implementation of BaseEmbeddingsModel for testing purposes."""

    def embed(self, embeddings_request: EmbeddingsRequest) -> EmbeddingsResponse:
        return EmbeddingsResponse(data=[], model="test-model", usage={"prompt_tokens": 10, "total_tokens": 10})  # noqa


@pytest.fixture
def chat_model():
    return ConcreteChatModel()


@pytest.fixture
def embeddings_model():
    return ConcreteEmbeddingsModel()


@pytest.fixture
def mock_chat_request():
    return Mock(spec=ChatRequest)


@pytest.fixture
def mock_chat_stream_response():
    mock = Mock(spec=ChatStreamResponse)
    mock.model_dump_json.return_value = '{"test": "data"}'
    return mock


@pytest.fixture
def mock_embeddings_request():
    return Mock(spec=EmbeddingsRequest)


def test_base_chat_model_list_models(chat_model):
    """Test that list_models returns an empty list by default."""
    # Act
    result = chat_model.list_models()

    # Assert
    assert isinstance(result, list)
    assert len(result) == 0


def test_base_chat_model_validate(chat_model, mock_chat_request):
    """Test that validate method doesn't raise exceptions by default."""
    # Act & Assert
    # This should not raise an exception
    chat_model.validate(mock_chat_request)


def test_base_chat_model_generate_message_id():
    """Test that generate_message_id returns a string with expected format."""
    # Act
    message_id = BaseChatModel.generate_message_id()

    # Assert
    assert isinstance(message_id, str)
    assert message_id.startswith("chatcmpl-")  # noqa
    assert len(message_id) == 17  # "chatcmpl-" (9) + 8 characters from uuid  # noqa


@patch('uuid.uuid4')
def test_base_chat_model_generate_message_id_with_mocked_uuid(mock_uuid4):
    """Test generate_message_id with a mocked UUID."""
    # Arrange
    mock_uuid4.return_value = uuid.UUID("12345678-1234-5678-9abc-123456789abc")

    # Act
    message_id = BaseChatModel.generate_message_id()

    # Assert
    assert message_id == "chatcmpl-12345678"  # noqa
    mock_uuid4.assert_called_once()


@patch('time.time')
def test_base_chat_model_stream_response_to_bytes_with_response(mock_time, mock_chat_stream_response):
    """Test stream_response_to_bytes with a ChatStreamResponse."""
    # Arrange
    mock_time.return_value = 1234567890

    # Act
    result = BaseChatModel.stream_response_to_bytes(mock_chat_stream_response)

    # Assert
    assert isinstance(result, bytes)
    assert b'data: {"test": "data"}\n\n' == result
    mock_chat_stream_response.model_dump_json.assert_called_once_with(exclude_unset=True)
    assert mock_chat_stream_response.system_fingerprint == "fp"
    assert mock_chat_stream_response.object == "chat.completion.chunk"
    assert mock_chat_stream_response.created == 1234567890


def test_base_chat_model_stream_response_to_bytes_without_response():
    """Test stream_response_to_bytes without a response."""
    # Act
    result = BaseChatModel.stream_response_to_bytes()

    # Assert
    assert isinstance(result, bytes)
    assert b'data: [DONE]\n\n' == result


@patch('time.time')
def test_stream_response_to_bytes_actual_json_formatting(mock_time):
    """Test that stream_response_to_bytes formats JSON data correctly."""
    # Arrange
    mock_time.return_value = 1234567890

    class MockStreamResponse:
        def __init__(self):
            self.field1 = "value1"
            self.field2 = "value2"
            self.system_fingerprint = None
            self.object = None
            self.created = None

        def model_dump_json(self, exclude_unset=False):  # noqa
            data = {
                "field1": "value1",
                "field2": "value2",
                "system_fingerprint": self.system_fingerprint,
                "object": self.object,
                "created": self.created
            }
            return json.dumps(data)

    mock_response = MockStreamResponse()

    # Act
    result = BaseChatModel.stream_response_to_bytes(mock_response)  # noqa

    # Assert
    assert b'data: ' in result
    expected_json_part = b'"field1":"value1"'
    assert expected_json_part.replace(b' ', b'') in result.replace(b' ', b'')


def test_base_embeddings_model_is_abstract():
    """Test that BaseEmbeddingsModel cannot be instantiated directly."""
    # Act & Assert
    with pytest.raises(TypeError):
        BaseEmbeddingsModel()


def test_base_chat_model_is_abstract():
    """Test that BaseChatModel cannot be instantiated directly."""
    # Act & Assert
    with pytest.raises(TypeError):
        BaseChatModel()


def test_concrete_embeddings_model_implementation(embeddings_model, mock_embeddings_request):
    """Test that a concrete implementation of BaseEmbeddingsModel works."""
    # Act
    with patch.object(ConcreteEmbeddingsModel, 'embed', return_value=EmbeddingsResponse(
            data=[],
            model="test-model",
            usage={"prompt_tokens": 10, "total_tokens": 10}  # noqa
    )):
        result = embeddings_model.embed(mock_embeddings_request)

    # Assert
    assert isinstance(result, EmbeddingsResponse)


def test_concrete_chat_model_implementation(chat_model, mock_chat_request):
    """Test that a concrete implementation of BaseChatModel works."""
    # Act
    with patch.object(ConcreteChatModel, 'chat', return_value=ChatResponse(
            choices=[],
            id="test-id",
            created=123,
            model="test-model",
            usage={  # noqa
                "prompt_tokens": 10,
                "completion_tokens": 20,
                "total_tokens": 30
            }
    )):
        result = chat_model.chat(mock_chat_request)

    # Assert
    assert isinstance(result, ChatResponse)


@pytest.mark.asyncio
async def test_concrete_chat_model_stream_implementation(chat_model, mock_chat_request):
    """Test that a concrete implementation of chat_stream works."""

    # For this test to run, you need pytest-asyncio installed
    # Act
    async def mock_stream():
        yield b"test stream data"

    with patch.object(ConcreteChatModel, 'chat_stream', return_value=mock_stream()):
        result = chat_model.chat_stream(mock_chat_request)

        # Assert
        assert hasattr(result, "__aiter__")

        # Verify we can iterate over the result
        data = []
        async for chunk in result:
            data.append(chunk)

        assert len(data) == 1
        assert data[0] == b"test stream data"
