import logging
from typing import Optional

from mcp.server.fastmcp import Context

# Import schemas and the client class definition (not the instance)
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
)
from .client import TelegramClientWrapper  # Import the class for type hinting
# Remove the circular import: from .server import telegram_wrapper_instance

logger = logging.getLogger(__name__)

# --- Helper Functions ---
# These helpers are used by the tool functions below


def _handle_error(tool_name: str, e: Exception) -> ErrorOutput:
    """Logs an error and returns a formatted ErrorOutput."""
    logger.error(f"Error in {tool_name} tool: {e}", exc_info=True)
    return ErrorOutput(error=f"An unexpected error occurred in {tool_name}: {str(e)}")


# Modify _check_client to accept context and retrieve client from state
async def _check_client(ctx: Context) -> Optional[ErrorOutput]:
    """Checks if the client instance is available, connected, and authorized via context state."""
    client_instance: Optional[TelegramClientWrapper] = getattr(
        ctx.app.state, "tg_client", None
    )

    if not client_instance:
        return ErrorOutput(
            error="Telegram client wrapper not initialized. Lifespan may have failed."
        )
    # Check connection status first
    try:
        # Use await here as is_connected might be async in some mock scenarios or future Telethon versions
        if (
            not client_instance.client
            or not await client_instance.client.is_connected()
        ):
            return ErrorOutput(
                error="Telegram client is not connected. Check server logs or restart."
            )
    except Exception as conn_err:
        logger.error(
            f"Error checking connection status in _check_client: {conn_err}",
            exc_info=True,
        )
        return ErrorOutput(error=f"Failed to check connection status: {str(conn_err)}")

    # Check authorization status
    try:
        if not await client_instance.client.is_user_authorized():
            return ErrorOutput(
                error="Telegram client connected but not authorized. Please run --login."
            )
    except Exception as auth_err:
        logger.error(
            f"Error checking authorization in _check_client: {auth_err}", exc_info=True
        )
        return ErrorOutput(
            error=f"Failed to check authorization status: {str(auth_err)}"
        )

    return None


# --- Tool Implementations ---
# These functions now access the client instance via ctx.app.state.tg_client


async def telegram_login_status_impl(
    ctx: Context,
) -> LoginStatusOutput:
    # This tool specifically checks status, so it gets the client instance directly
    # It should work even if the client isn't fully authorized yet.
    client_instance: Optional[TelegramClientWrapper] = getattr(
        ctx.app.state, "tg_client", None
    )
    # Create a temporary wrapper if none exists (e.g., server failed during lifespan)
    # This might hide issues; better to rely on lifespan providing the instance.
    # If instance is None, get_login_status should handle it.
    checker = (
        client_instance or TelegramClientWrapper()
    )  # checker might be a new instance if client_instance is None
    try:
        # Use the checker's method
        status = await checker.get_login_status()
        # Ensure the return type matches LoginStatusOutput schema
        # The get_login_status method should return a dict matching the schema fields
        return LoginStatusOutput(**status)
    except Exception as e:
        logger.error(f"Error getting login status via tool: {e}", exc_info=True)
        # Attempt to determine connection status even on error
        connected = False
        if checker and checker.client:
            try:
                # Add await here as is_connected() might be async
                connected = await checker.client.is_connected()
            except Exception:  # Ignore errors checking connection after another error
                logger.warning(
                    "Ignoring error during connection check within exception handler."
                )
                pass
        return LoginStatusOutput(
            connected=connected,  # Pass the boolean result
            authorized=False,
            message=f"Error checking status: {str(e)}",
        )


async def telegram_list_chats_impl(
    ctx: Context, args: TelegramListChatsInput
) -> MaybeErrorList:
    # Use the helper which now checks auth via context
    if error := await _check_client(ctx):
        return error
    client_instance: TelegramClientWrapper = ctx.app.state.tg_client
    try:
        results = await client_instance.list_chats(limit=args.limit)
        return results
    except Exception as e:  # Catch exceptions raised by the wrapper method
        return _handle_error("telegram_list_chats", e)


async def telegram_search_chats_impl(
    ctx: Context, args: TelegramSearchChatsInput
) -> MaybeErrorList:
    if error := await _check_client(ctx):
        return error
    client_instance: TelegramClientWrapper = ctx.app.state.tg_client
    try:
        results = await client_instance.search_chats(args.query)
        return results
    except Exception as e:
        return _handle_error("telegram_search_chats", e)


async def telegram_post_message_impl(
    ctx: Context, args: TelegramPostMessageInput
) -> PostMessageOutput:
    # Check client status (includes auth check now)
    if error := await _check_client(ctx):
        return PostMessageOutput(status="failed", error=error.error)
    client_instance: TelegramClientWrapper = ctx.app.state.tg_client
    try:
        # The wrapper method should ideally return a dict matching the schema or raise an exception
        result_dict = await client_instance.post_message(args.chat_id, args.text)
        # Validate and return the Pydantic model
        return PostMessageOutput(**result_dict)
    except Exception as e:
        # Handle exceptions raised from the client wrapper or validation errors
        err_out = _handle_error("telegram_post_message", e)
        return PostMessageOutput(status="failed", error=err_out.error)


async def telegram_reply_to_message_impl(
    ctx: Context, args: TelegramReplyToMessageInput
) -> ReplyMessageOutput:
    if error := await _check_client(ctx):
        return ReplyMessageOutput(status="failed", error=error.error)
    client_instance: TelegramClientWrapper = ctx.app.state.tg_client
    try:
        result_dict = await client_instance.reply_to_message(
            args.chat_id, args.message_id, args.text
        )
        return ReplyMessageOutput(**result_dict)
    except Exception as e:
        err_out = _handle_error("telegram_reply_to_message", e)
        return ReplyMessageOutput(status="failed", error=err_out.error)


async def telegram_add_reaction_impl(
    ctx: Context, args: TelegramAddReactionInput
) -> AddReactionOutput:
    if error := await _check_client(ctx):
        return AddReactionOutput(status="failed", error=error.error)
    client_instance: TelegramClientWrapper = ctx.app.state.tg_client
    try:
        result_dict = await client_instance.add_reaction(
            args.chat_id, args.message_id, args.reaction
        )
        return AddReactionOutput(**result_dict)
    except Exception as e:
        err_out = _handle_error("telegram_add_reaction", e)
        return AddReactionOutput(status="failed", error=err_out.error)


async def telegram_get_chat_history_impl(
    ctx: Context, args: TelegramGetChatHistoryInput
) -> MaybeErrorList:
    if error := await _check_client(ctx):
        return error
    client_instance: TelegramClientWrapper = ctx.app.state.tg_client
    try:
        messages = await client_instance.get_chat_history(
            args.chat_id, args.limit, args.max_id
        )
        return messages
    except Exception as e:
        return _handle_error("telegram_get_chat_history", e)


async def telegram_get_user_profile_impl(
    ctx: Context, args: TelegramGetUserProfileInput
) -> MaybeErrorDict:
    if error := await _check_client(ctx):
        return error
    client_instance: TelegramClientWrapper = ctx.app.state.tg_client
    try:
        profile = await client_instance.get_user_profile(args.user_id)
        # Check if the wrapper returned an error dict
        if isinstance(profile, dict) and "error" in profile:
            return ErrorOutput(error=profile["error"])
        return profile  # Return the dict directly
    except Exception as e:
        return _handle_error("telegram_get_user_profile", e)


async def search_telegram_messages_impl(
    ctx: Context, args: TelegramSearchMessagesInput
) -> MaybeErrorList:
    if error := await _check_client(ctx):
        return error
    client_instance: TelegramClientWrapper = ctx.app.state.tg_client
    try:
        results = await client_instance.search_messages(
            query=args.query, chat_id=args.chat_id, limit=args.limit
        )
        return results
    except Exception as e:
        return _handle_error("search_telegram_messages", e)
