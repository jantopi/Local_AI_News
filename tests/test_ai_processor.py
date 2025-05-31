import pytest
import requests
from unittest.mock import patch, MagicMock
from ai_processor.processor import summarize_text, OLLAMA_API_URL, DEFAULT_MODEL

MOCK_OLLAMA_SUCCESS_RESPONSE = {
    "model": DEFAULT_MODEL,
    "created_at": "2024-07-23T12:00:00.000Z",
    "response": "This is a mock AI summary.",
    "done": True
}

MOCK_OLLAMA_EMPTY_RESPONSE = {
    "model": DEFAULT_MODEL,
    "created_at": "2024-07-23T12:00:00.000Z",
    "response": "", # Empty response
    "done": True
}

MOCK_OLLAMA_SHORT_RESPONSE = {
    "model": DEFAULT_MODEL,
    "created_at": "2024-07-23T12:00:00.000Z",
    "response": "Short.", # Too short to be a good summary
    "done": True
}

@patch('requests.post')
def test_summarize_text_success(mock_post):
    """Test successful text summarization with a mocked Ollama API call."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_OLLAMA_SUCCESS_RESPONSE
    mock_post.return_value = mock_response

    summary = summarize_text("This is a sample news article to be summarized.")

    assert summary == "This is a mock AI summary."
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert args[0] == OLLAMA_API_URL
    assert kwargs['json']['model'] == DEFAULT_MODEL
    assert "Summarize the following news article" in kwargs['json']['prompt']

@patch('requests.post')
def test_summarize_text_api_error(mock_post):
    """Test text summarization when the Ollama API returns an HTTP error."""
    mock_response = MagicMock()
    mock_response.status_code = 500 # Internal Server Error
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("API Error")
    mock_post.return_value = mock_response

    summary = summarize_text("Another article.")
    assert summary is None
    mock_post.assert_called_once()

@patch('requests.post')
def test_summarize_text_connection_error(mock_post):
    """Test text summarization when there's a connection error to Ollama API."""
    mock_post.side_effect = requests.exceptions.ConnectionError("Failed to connect")

    summary = summarize_text("Text that won't be summarized.")
    assert summary is None
    mock_post.assert_called_once()

@patch('requests.post')
def test_summarize_text_empty_response_from_model(mock_post):
    """Test when the model returns an empty string as a summary."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_OLLAMA_EMPTY_RESPONSE
    mock_post.return_value = mock_response

    summary = summarize_text("Some text.")
    assert summary is None # Should be None as empty string is not a valid summary

@patch('requests.post')
def test_summarize_text_too_short_response_from_model(mock_post):
    """Test when the model returns a very short, likely meaningless, summary."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_OLLAMA_SHORT_RESPONSE # "Short."
    mock_post.return_value = mock_response

    summary = summarize_text("A long piece of text that needs a good summary.")
    assert summary is None # Should be None as "Short." is not a valid summary based on length check

def test_summarize_text_empty_input_text():
    """Test summarizing with empty input text."""
    summary = summarize_text("")
    assert summary is None

def test_summarize_text_none_input_text():
    """Test summarizing with None as input text."""
    summary = summarize_text(None)
    assert summary is None

@patch('requests.post')
def test_summarize_text_custom_model(mock_post):
    """Test successful text summarization with a custom model name."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_OLLAMA_SUCCESS_RESPONSE
    mock_post.return_value = mock_response

    custom_model_name = "custom:gemma-model"
    summary = summarize_text("This is a sample news article.", model=custom_model_name)

    assert summary == "This is a mock AI summary."
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs['json']['model'] == custom_model_name

@patch('requests.post')
def test_summarize_text_json_decode_error(mock_post):
    """Test text summarization when the Ollama API returns invalid JSON."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "This is not valid JSON"
    mock_response.json.side_effect = requests.exceptions.JSONDecodeError("Error decoding JSON", "doc", 0)
    mock_post.return_value = mock_response

    summary = summarize_text("Article text for JSON error test.")
    assert summary is None
    mock_post.assert_called_once()

# To run these tests, navigate to the project root and run:
# python -m pytest
```
