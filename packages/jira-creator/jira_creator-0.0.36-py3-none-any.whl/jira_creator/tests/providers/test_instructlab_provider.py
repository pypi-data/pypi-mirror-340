from unittest.mock import MagicMock, patch

import pytest
from providers.instructlab_provider import InstructLabProvider


def test_instructlab_provider_init_defaults():
    with patch.dict(
        "os.environ", {}, clear=True
    ):  # Clear any existing environment variables
        provider = InstructLabProvider()
        assert provider.url == "http://localhost:11434/api/generate"
        assert provider.model == "instructlab"


def test_instructlab_provider_init_env():
    with patch.dict(
        "os.environ", {"AI_URL": "http://custom-url", "AI_MODEL": "custom-model"}
    ):
        provider = InstructLabProvider()
        assert provider.url == "http://custom-url"
        assert provider.model == "custom-model"


def test_improve_text_success():
    provider = InstructLabProvider()

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"response": " Improved text "}

    with patch(
        "providers.instructlab_provider.requests.post", return_value=mock_response
    ) as mock_post:
        result = provider.improve_text("Prompt", "Input text")

    assert result == "Improved text"
    mock_post.assert_called_once()
    assert "Prompt\n\nInput text" in mock_post.call_args[1]["json"]["prompt"]


def test_improve_text_failure():
    provider = InstructLabProvider()

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Server error"

    with patch(
        "providers.instructlab_provider.requests.post", return_value=mock_response
    ):
        with pytest.raises(Exception) as exc_info:
            provider.improve_text("Prompt", "Input text")

    assert "InstructLab request failed: 500 - Server error" in str(exc_info.value)
