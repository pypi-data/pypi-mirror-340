import logging
from typing import Optional

from mcp.server.fastmcp import Context

# Import schemas and the client class definition
from .schemas import (
    ErrorOutput,
    LoginStatusOutput,
    TelegramListChatsInput,
    MaybeErrorList,
    TelegramSearchChatsInput,
    TelegramPostMessageInput,
    PostMessageOutput,
    TelegramReplyToMessageInput,
    ReplyMessageOutput,
    TelegramAddReactionInput,
    AddReactionOutput,
    TelegramGetChatHistoryInput,
    TelegramGetUserProfileInput,
    MaybeErrorDict,
    TelegramSearchMessagesInput,
    TelegramLoginStatusInput,  # Added import
)

# Import the global instance from client.py
from .client import telegram_wrapper_instance

logger = logging.getLogger(__name__)

# --- Helper Functions (Moved back here) ---


def _handle_error(tool_name: str, e: Exception) -> ErrorOutput:
    """Logs an error and returns a formatted ErrorOutput."""
    logger.error(f"Error in {tool_name} tool: {e}", exc_info=True)
    return ErrorOutput(error=f"An unexpected error occurred in {tool_name}: {str(e)}")


# Modify _check_client to use the global instance from client.py
async def _check_client() -> Optional[ErrorOutput]:
    """Checks if the global client instance is available, connected, and authorized."""
    if not telegram_wrapper_instance:
        return ErrorOutput(
            error="Telegram client wrapper not initialized. Lifespan may have failed."
        )
    try:
        # Use await for async checks
        if (
            not telegram_wrapper_instance.client
            or not await telegram_wrapper_instance.client.is_connected()
        ):
            return ErrorOutput(
                error="Telegram client is not connected. Check server logs or restart."
            )
        if not await telegram_wrapper_instance.client.is_user_authorized():
            return ErrorOutput(
                error="Telegram client connected but not authorized. Please run --login."
            )
    except Exception as err:
        logger.error(
            f"Error checking client status in _check_client: {err}", exc_info=True
        )
        return ErrorOutput(error=f"Failed to check client status: {str(err)}")

    return None


# --- Tool Implementations ---
# These functions now access the client instance via the imported global telegram_wrapper_instance


async def telegram_login_status_impl(
    ctx: Context,
    args: TelegramLoginStatusInput,  # Added args parameter
) -> LoginStatusOutput:
    # args is unused but required by the signature for FastMCP
    checker = telegram_wrapper_instance
    if not checker:
        return LoginStatusOutput(
            connected=False,
            authorized=False,
            message="Client instance not available (lifespan error?).",
        )

    try:
        status = await checker.get_login_status()
        return LoginStatusOutput(**status)
    except Exception as e:
        logger.error(f"Error getting login status via tool: {e}", exc_info=True)
        connected = False
        if checker and checker.client:
            try:
                connected = await checker.client.is_connected()
            except Exception:
                pass
        return LoginStatusOutput(
            connected=connected,
            authorized=False,
            message=f"Error checking status: {str(e)}",
        )


async def telegram_list_chats_impl(
    ctx: Context, args: TelegramListChatsInput
) -> MaybeErrorList:
    if error := await _check_client():
        return error
    try:
        results = await telegram_wrapper_instance.list_chats(limit=args.limit)
        return results
    except Exception as e:
        return _handle_error("telegram_list_chats", e)


async def telegram_search_chats_impl(
    ctx: Context, args: TelegramSearchChatsInput
) -> MaybeErrorList:
    if error := await _check_client():
        return error
    try:
        results = await telegram_wrapper_instance.search_chats(args.query)
        return results
    except Exception as e:
        return _handle_error("telegram_search_chats", e)


async def telegram_post_message_impl(
    ctx: Context, args: TelegramPostMessageInput
) -> PostMessageOutput:
    if error := await _check_client():
        return PostMessageOutput(status="failed", error=error.error)
    try:
        result_dict = await telegram_wrapper_instance.post_message(
            args.chat_id, args.text
        )
        return PostMessageOutput(**result_dict)
    except Exception as e:
        err_out = _handle_error("telegram_post_message", e)
        return PostMessageOutput(status="failed", error=err_out.error)


async def telegram_reply_to_message_impl(
    ctx: Context, args: TelegramReplyToMessageInput
) -> ReplyMessageOutput:
    if error := await _check_client():
        return ReplyMessageOutput(status="failed", error=error.error)
    try:
        result_dict = await telegram_wrapper_instance.reply_to_message(
            args.chat_id, args.message_id, args.text
        )
        return ReplyMessageOutput(**result_dict)
    except Exception as e:
        err_out = _handle_error("telegram_reply_to_message", e)
        return ReplyMessageOutput(status="failed", error=err_out.error)


async def telegram_add_reaction_impl(
    ctx: Context, args: TelegramAddReactionInput
) -> AddReactionOutput:
    if error := await _check_client():
        return AddReactionOutput(status="failed", error=error.error)
    try:
        result_dict = await telegram_wrapper_instance.add_reaction(
            args.chat_id, args.message_id, args.reaction
        )
        return AddReactionOutput(**result_dict)
    except Exception as e:
        err_out = _handle_error("telegram_add_reaction", e)
        return AddReactionOutput(status="failed", error=err_out.error)


async def telegram_get_chat_history_impl(
    ctx: Context, args: TelegramGetChatHistoryInput
) -> MaybeErrorList:
    if error := await _check_client():
        return error
    try:
        messages = await telegram_wrapper_instance.get_chat_history(
            args.chat_id, args.limit, args.max_id
        )
        return messages
    except Exception as e:
        return _handle_error("telegram_get_chat_history", e)


async def telegram_get_user_profile_impl(
    ctx: Context, args: TelegramGetUserProfileInput
) -> MaybeErrorDict:
    if error := await _check_client():
        return error
    try:
        profile = await telegram_wrapper_instance.get_user_profile(args.user_id)
        if isinstance(profile, dict) and "error" in profile:
            return ErrorOutput(error=profile["error"])
        return profile
    except Exception as e:
        return _handle_error("telegram_get_user_profile", e)


async def search_telegram_messages_impl(
    ctx: Context, args: TelegramSearchMessagesInput
) -> MaybeErrorList:
    if error := await _check_client():
        return error
    try:
        results = await telegram_wrapper_instance.search_messages(
            query=args.query, chat_id=args.chat_id, limit=args.limit
        )
        return results
    except Exception as e:
        return _handle_error("search_telegram_messages", e)
