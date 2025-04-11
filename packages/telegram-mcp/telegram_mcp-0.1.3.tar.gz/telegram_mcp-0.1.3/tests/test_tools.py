# telegram_mcp_server/tests/test_tools.py
import pytest
from unittest.mock import AsyncMock

# Import tool *implementations* from the new tools module
from telegram_mcp.tools import telegram_login_status_impl, telegram_post_message_impl

# Import schemas for creating input arguments and checking output types
from telegram_mcp.schemas import (
    TelegramPostMessageInput,
    LoginStatusOutput,
    PostMessageOutput,
)
# Import Context for type hinting (though we use a mock)

# Mark all tests in this module to use anyio for async execution
pytestmark = pytest.mark.anyio

# --- Tests for telegram_login_status ---


async def test_login_status_connected_authorized(mock_context):
    """Test login status when connected and authorized."""
    mock_wrapper = mock_context.app.state.tg_client
    status: LoginStatusOutput = await telegram_login_status_impl(mock_context)

    assert isinstance(status, LoginStatusOutput)
    assert status.connected is True
    assert status.authorized is True
    assert status.user is not None
    assert status.user.username == "testuser"
    assert status.user.id == 12345
    mock_wrapper.get_login_status.assert_awaited_once()


async def test_login_status_connected_not_authorized(mock_context):
    """Test login status when connected but not authorized."""
    mock_wrapper = mock_context.app.state.tg_client
    mock_wrapper.client.is_user_authorized.return_value = False
    status: LoginStatusOutput = await telegram_login_status_impl(mock_context)

    assert isinstance(status, LoginStatusOutput)
    assert status.connected is True
    assert status.authorized is False
    assert status.user is None
    mock_wrapper.get_login_status.assert_awaited_once()


async def test_login_status_not_connected(mock_context):
    """Test login status when not connected."""
    mock_wrapper = mock_context.app.state.tg_client
    mock_wrapper.client.is_connected.return_value = False
    mock_wrapper.client.is_user_authorized.return_value = False
    status: LoginStatusOutput = await telegram_login_status_impl(mock_context)

    assert isinstance(status, LoginStatusOutput)
    assert status.connected is False
    assert status.authorized is False
    assert status.user is None
    mock_wrapper.get_login_status.assert_awaited_once()


# --- Tests for telegram_post_message ---


async def test_post_message_success(mock_context):
    """Test successful message posting."""
    mock_wrapper = mock_context.app.state.tg_client
    args = TelegramPostMessageInput(chat_id="test_chat", text="Hello, world!")
    result: PostMessageOutput = await telegram_post_message_impl(mock_context, args)

    assert isinstance(result, PostMessageOutput)
    assert result.status == "success"
    assert result.message_id == 9876
    mock_wrapper.post_message.assert_awaited()
    # Use positional arguments in assertion to match the call
    mock_wrapper.post_message.assert_called_once_with(args.chat_id, args.text)


async def test_post_message_failure_api_error(mock_context):
    """Test message posting failure due to API error simulated by the wrapper."""
    mock_wrapper = mock_context.app.state.tg_client
    args = TelegramPostMessageInput(chat_id="test_chat", text="Hello, failure!")
    error_response = {"status": "failed", "error": "Invalid chat ID"}
    mock_wrapper.post_message.side_effect = AsyncMock(return_value=error_response)

    result: PostMessageOutput = await telegram_post_message_impl(mock_context, args)

    assert isinstance(result, PostMessageOutput)
    assert result.status == "failed"
    assert result.error == "Invalid chat ID"
    mock_wrapper.post_message.assert_awaited()
    # Use positional arguments in assertion to match the call
    mock_wrapper.post_message.assert_called_once_with(args.chat_id, args.text)


async def test_post_message_failure_exception(mock_context):
    """Test message posting failure due to an exception raised by the wrapper."""
    mock_wrapper = mock_context.app.state.tg_client
    args = TelegramPostMessageInput(chat_id="test_chat", text="Hello, exception!")
    mock_wrapper.post_message.side_effect = Exception("Network error")

    result: PostMessageOutput = await telegram_post_message_impl(mock_context, args)

    assert isinstance(result, PostMessageOutput)
    assert result.status == "failed"
    assert "Network error" in result.error
    mock_wrapper.post_message.assert_awaited()
    # Use positional arguments in assertion to match the call
    mock_wrapper.post_message.assert_called_once_with(args.chat_id, args.text)


async def test_post_message_not_connected(mock_context):
    """Test posting message when not connected."""
    mock_wrapper = mock_context.app.state.tg_client
    mock_wrapper.client.is_connected.return_value = False
    mock_wrapper.client.is_user_authorized.return_value = False
    mock_wrapper._ensure_connected.side_effect = ConnectionError(
        "Telegram client is not connected."
    )

    args = TelegramPostMessageInput(chat_id="test_chat", text="Cannot send")
    # Need to await _check_client within the tool impl to catch the error
    result = await telegram_post_message_impl(mock_context, args)

    assert isinstance(result, PostMessageOutput)
    assert result.status == "failed"
    # Check the specific error raised by _ensure_connected via _check_client
    # The error comes from _check_client now
    assert "client is not connected" in result.error.lower()
    mock_wrapper.post_message.assert_not_awaited()


async def test_post_message_not_authorized(mock_context):
    """Test posting message when connected but not authorized."""
    mock_wrapper = mock_context.app.state.tg_client
    mock_wrapper.client.is_connected.return_value = True
    mock_wrapper.client.is_user_authorized.return_value = False
    # Ensure _ensure_connected mock raises correctly
    mock_wrapper._ensure_connected.side_effect = ConnectionError(
        "Telegram client connected but not authorized."
    )

    args = TelegramPostMessageInput(chat_id="test_chat", text="Cannot send")
    # Need to await _check_client within the tool impl to catch the error
    result = await telegram_post_message_impl(mock_context, args)

    assert isinstance(result, PostMessageOutput)
    assert result.status == "failed"
    # Check the specific error raised by _ensure_connected via _check_client
    # The error comes from _check_client now
    assert "not authorized" in result.error.lower()
    mock_wrapper.post_message.assert_not_awaited()


# TODO: Add tests for other tool implementations (list_chats, search_chats, etc.)
