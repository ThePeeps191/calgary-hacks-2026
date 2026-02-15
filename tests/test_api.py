import pytest
import json
import io
import os
import sys
from unittest.mock import patch

# Add project root to path so we can import main
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

TEST_AUDIO_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "user_downloads",
    "test_audio.m4a"
)


class MockParagraph:
    def __init__(self, text, is_biased=False, replacement="", reason=""):
        self.text = text
        self.is_text_biased_enough = is_biased
        self.unbiased_replacement = replacement
        self.reason_biased = reason


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ── Test 1: No file provided ──────────────────────────────────────────────────

def test_fetch_audio_no_file(client):
    """POST with no file attached should return 400."""
    response = client.post("/fetch-audio")
    data = json.loads(response.data)
    assert response.status_code == 400
    assert data["status"] == "error"
    assert "No file provided" in data["message"]


# ── Test 2: Empty filename ────────────────────────────────────────────────────

def test_fetch_audio_empty_filename(client):
    """POST with a file field but empty filename should return 400."""
    data = {"file": (io.BytesIO(b""), "")}
    response = client.post("/fetch-audio", content_type="multipart/form-data", data=data)
    result = json.loads(response.data)
    assert response.status_code == 400
    assert result["status"] == "error"
    assert "No file selected" in result["message"]


# ── Test 3: Full pipeline with mocked dependencies ────────────────────────────

def test_fetch_audio_mocked_pipeline(client):
    """Upload test_audio.m4a with mocked transcription and bias pipeline."""
    sample_text = "Politicians are destroying our country with corrupt policies."
    mock_paragraphs = [
        MockParagraph(
            text=sample_text,
            is_biased=True,
            replacement="Politicians are implementing controversial policies.",
            reason="Uses emotionally charged language: 'destroying', 'corrupt'.",
        )
    ]

    assert os.path.exists(TEST_AUDIO_PATH), f"test_audio.m4a not found at {TEST_AUDIO_PATH}"

    with patch("media.audio_to_text", return_value=sample_text), \
         patch("bias.segment_paragraphs", return_value=mock_paragraphs):

        with open(TEST_AUDIO_PATH, "rb") as f:
            file_data = {"file": (f, "test_audio.m4a")}
            response = client.post(
                "/fetch-audio",
                content_type="multipart/form-data",
                data=file_data,
            )

    result = json.loads(response.data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {result}"
    assert result["status"] == "ok"
    assert "data" in result

    payload = result["data"]
    assert payload["text"] == sample_text
    assert isinstance(payload["paragraphs"], list)
    assert len(payload["paragraphs"]) == 1

    para = payload["paragraphs"][0]
    assert para["text"] == sample_text
    assert para["bias_score"] is True
    assert "unbiased_replacement" in para
    assert "reason_biased" in para


# ── Test 4: Transcription error propagates correctly ──────────────────────────

def test_fetch_audio_transcription_error(client):
    """When audio_to_text returns an Error: prefix, endpoint should return 500."""
    with patch("media.audio_to_text", return_value="Error: Could not understand audio"):
        assert os.path.exists(TEST_AUDIO_PATH)
        with open(TEST_AUDIO_PATH, "rb") as f:
            file_data = {"file": (f, "test_audio.m4a")}
            response = client.post(
                "/fetch-audio",
                content_type="multipart/form-data",
                data=file_data,
            )

    result = json.loads(response.data)
    assert response.status_code == 500
    assert result["status"] == "error"
    assert "Error" in result["message"]


# ── Test 5: Real transcription (mocks only the bias pipeline) ─────────────────

def test_fetch_audio_real_transcription(client):
    """
    Integration test: actually transcribes test_audio.m4a via Google Speech API.
    Mocks only bias.segment_paragraphs to avoid slow Gemini calls.
    Verifies transcription returns non-empty text and pipeline completes.
    """
    assert os.path.exists(TEST_AUDIO_PATH), f"test_audio.m4a not found at {TEST_AUDIO_PATH}"

    # We let audio_to_text run for real; mock segment_paragraphs so we don't
    # spend time on Gemini bias calls during the test run.
    def fake_segment(text):
        return [MockParagraph(text=text, is_biased=False)]

    with patch("bias.segment_paragraphs", side_effect=fake_segment):
        with open(TEST_AUDIO_PATH, "rb") as f:
            file_data = {"file": (f, "test_audio.m4a")}
            response = client.post(
                "/fetch-audio",
                content_type="multipart/form-data",
                data=file_data,
            )

    result = json.loads(response.data)
    # Either 200 (transcription succeeded) or 500 with error message
    if response.status_code == 200:
        assert result["status"] == "ok"
        assert len(result["data"]["text"]) > 0, "Transcription returned empty text"
        assert isinstance(result["data"]["paragraphs"], list)
    else:
        # Transcription failure is acceptable in CI (no microphone / network)
        assert result["status"] == "error"
        assert result["message"].startswith("Error:")
