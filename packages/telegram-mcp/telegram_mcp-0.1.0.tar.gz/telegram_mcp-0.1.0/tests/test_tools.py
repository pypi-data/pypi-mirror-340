# telegram_mcp_server/tests/test_tools.py
import pytest
from unittest.mock import AsyncMock

# Assuming the tool functions are directly available in telegram_mcp_runner
# Adjust the import path if the functions are located elsewhere
from telegram_mcp_runner import telegram_login_status, telegram_post_message

# Mark all tests in this module to use anyio for async execution
pytestmark = pytest.mark.anyio

# --- Tests for telegram_login_status ---


async def test_login_status_connected_authorized(mock_telegram_wrapper):
    """Test login status when connected and authorized."""
    # Fixture default state is connected and authorized
    status = await telegram_login_status()
    assert status["connected"] is True
    assert status["authorized"] is True
    assert status["user_info"] is not None
    assert status["user_info"]["username"] == "testuser"
    assert status["user_info"]["id"] == 12345
    mock_telegram_wrapper.get_login_status.assert_awaited_once()


async def test_login_status_connected_not_authorized(mock_telegram_wrapper):
    """Test login status when connected but not authorized."""
    mock_telegram_wrapper.is_user_authorized.return_value = False

    # Re-configure the side effect to pick up the change
    async def mock_get_login_status_updated():
        return {
            "connected": True,
            "authorized": False,
            "user_info": None,
        }

    mock_telegram_wrapper.get_login_status = AsyncMock(
        side_effect=mock_get_login_status_updated
    )

    status = await telegram_login_status()
    assert status["connected"] is True
    assert status["authorized"] is False
    assert status["user_info"] is None
    mock_telegram_wrapper.get_login_status.assert_awaited_once()


async def test_login_status_not_connected(mock_telegram_wrapper):
    """Test login status when not connected."""
    mock_telegram_wrapper.is_connected.return_value = False
    mock_telegram_wrapper.is_user_authorized.return_value = (
        False  # Typically also false if not connected
    )

    # Re-configure the side effect to pick up the change
    async def mock_get_login_status_updated():
        return {
            "connected": False,
            "authorized": False,
            "user_info": None,
        }

    mock_telegram_wrapper.get_login_status = AsyncMock(
        side_effect=mock_get_login_status_updated
    )

    status = await telegram_login_status()
    assert status["connected"] is False
    assert status["authorized"] is False
    assert status["user_info"] is None
    mock_telegram_wrapper.get_login_status.assert_awaited_once()


# --- Tests for telegram_post_message ---


async def test_post_message_success(mock_telegram_wrapper):
    """Test successful message posting."""
    chat_id = "test_chat"
    text = "Hello, world!"
    # Default mock behavior is success
    result = await telegram_post_message(chat_id=chat_id, text=text)

    assert result["status"] == "success"
    assert result["message_id"] == 9876
    mock_telegram_wrapper.post_message.assert_awaited_once_with(
        chat_id=chat_id, text=text
    )


async def test_post_message_failure_api_error(mock_telegram_wrapper):
    """Test message posting failure due to API error."""
    chat_id = "test_chat"
    text = "Hello, failure!"
    error_response = {"status": "error", "error": "Invalid chat ID"}
    mock_telegram_wrapper.post_message.return_value = error_response

    result = await telegram_post_message(chat_id=chat_id, text=text)

    assert result["status"] == "error"
    assert result["error"] == "Invalid chat ID"
    mock_telegram_wrapper.post_message.assert_awaited_once_with(
        chat_id=chat_id, text=text
    )


async def test_post_message_failure_exception(mock_telegram_wrapper):
    """Test message posting failure due to an exception."""
    chat_id = "test_chat"
    text = "Hello, exception!"
    mock_telegram_wrapper.post_message.side_effect = Exception("Network error")

    # Expecting the tool function to catch the exception and return an error dict
    result = await telegram_post_message(chat_id=chat_id, text=text)

    assert result["status"] == "error"
    assert "Network error" in result["error"]  # Check if exception message is included
    mock_telegram_wrapper.post_message.assert_awaited_once_with(
        chat_id=chat_id, text=text
    )


async def test_post_message_not_connected(mock_telegram_wrapper):
    """Test posting message when not connected."""
    mock_telegram_wrapper.is_connected.return_value = False
    mock_telegram_wrapper.is_user_authorized.return_value = False

    chat_id = "test_chat"
    text = "Cannot send"
    result = await telegram_post_message(chat_id=chat_id, text=text)

    assert result["status"] == "error"
    assert "Telegram client not connected or authorized" in result["error"]
    mock_telegram_wrapper.post_message.assert_not_awaited()  # Should not attempt to send


async def test_post_message_not_authorized(mock_telegram_wrapper):
    """Test posting message when connected but not authorized."""
    mock_telegram_wrapper.is_connected.return_value = True
    mock_telegram_wrapper.is_user_authorized.return_value = False

    chat_id = "test_chat"
    text = "Cannot send"
    result = await telegram_post_message(chat_id=chat_id, text=text)

    assert result["status"] == "error"
    assert "Telegram client not connected or authorized" in result["error"]
    mock_telegram_wrapper.post_message.assert_not_awaited()  # Should not attempt to send
