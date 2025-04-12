import logging
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP, Context

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
    TelegramLoginStatusInput,
)

# Import the global instance and class from client.py
from . import client  # Import client module to update global instance
# from .client import telegram_wrapper_instance # Direct import for use

logger = logging.getLogger(__name__)

# --- Lifespan Management (Moved from server.py) ---


@asynccontextmanager
async def lifespan(app: FastMCP) -> AsyncGenerator[None, None]:
    """Manages the Telegram client connection lifecycle for the running server."""
    logger.info("MCP Server lifespan starting...")
    if client.telegram_wrapper_instance is not None:
        logger.warning(
            "Lifespan started but telegram_wrapper_instance was not None. Resetting."
        )
        client.telegram_wrapper_instance = None

    wrapper = client.TelegramClientWrapper()
    try:
        logger.info("Connecting Telegram client using existing session...")
        connected = await wrapper.connect(perform_login_if_needed=False)
        if connected:
            client.telegram_wrapper_instance = wrapper
            logger.info("Telegram client connected and authorized via session.")
        else:
            logger.warning(
                "Lifespan: Failed to connect/authorize. Tools requiring auth will fail."
            )
            client.telegram_wrapper_instance = wrapper
        yield
    except Exception as e:
        logger.error(f"FATAL: Exception during lifespan connection: {e}", exc_info=True)
        client.telegram_wrapper_instance = None
        raise
    finally:
        logger.info("MCP Server lifespan ending...")
        if client.telegram_wrapper_instance:
            logger.info("Disconnecting client during lifespan shutdown...")
            await client.telegram_wrapper_instance.disconnect()
            client.telegram_wrapper_instance = None


# --- FastMCP Server Instance (Moved from server.py) ---
mcp = FastMCP(lifespan=lifespan)


# --- Helper Functions ---


def _handle_error(tool_name: str, e: Exception) -> ErrorOutput:
    """Logs an error and returns a formatted ErrorOutput."""
    logger.error(f"Error in {tool_name} tool: {e}", exc_info=True)
    return ErrorOutput(error=f"An unexpected error occurred in {tool_name}: {str(e)}")


async def _check_client() -> Optional[ErrorOutput]:
    """Checks if the global client instance is available, connected, and authorized."""
    # Use the instance imported from client module
    if not client.telegram_wrapper_instance:
        return ErrorOutput(
            error="Telegram client wrapper not initialized. Lifespan may have failed."
        )
    try:
        if (
            not client.telegram_wrapper_instance.client
            or not await client.telegram_wrapper_instance.client.is_connected()
        ):
            return ErrorOutput(
                error="Telegram client is not connected. Check server logs or restart."
            )
        if not await client.telegram_wrapper_instance.client.is_user_authorized():
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

# Note: We register these implementations directly now


@mcp.tool(
    name="telegram_login_status",
    description="Checks the current connection and authorization status.",
)
async def telegram_login_status_impl(
    ctx: Context, args: TelegramLoginStatusInput
) -> LoginStatusOutput:
    checker = client.telegram_wrapper_instance
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


@mcp.tool(
    name="telegram_list_chats",
    description="Lists recent chats, channels, and conversations.",
)
async def telegram_list_chats_impl(
    ctx: Context, args: TelegramListChatsInput
) -> MaybeErrorList:
    if error := await _check_client():
        return error
    try:
        results = await client.telegram_wrapper_instance.list_chats(limit=args.limit)
        return results
    except Exception as e:
        return _handle_error("telegram_list_chats", e)


@mcp.tool(
    name="telegram_search_chats",
    description="Searches chats, channels, or users by name.",
)
async def telegram_search_chats_impl(
    ctx: Context, args: TelegramSearchChatsInput
) -> MaybeErrorList:
    if error := await _check_client():
        return error
    try:
        results = await client.telegram_wrapper_instance.search_chats(args.query)
        return results
    except Exception as e:
        return _handle_error("telegram_search_chats", e)


@mcp.tool(
    name="telegram_post_message",
    description="Sends a text message.",
)
async def telegram_post_message_impl(
    ctx: Context, args: TelegramPostMessageInput
) -> PostMessageOutput:
    if error := await _check_client():
        return PostMessageOutput(status="failed", error=error.error)
    try:
        result_dict = await client.telegram_wrapper_instance.post_message(
            args.chat_id, args.text
        )
        return PostMessageOutput(**result_dict)
    except Exception as e:
        err_out = _handle_error("telegram_post_message", e)
        return PostMessageOutput(status="failed", error=err_out.error)


@mcp.tool(
    name="telegram_reply_to_message",
    description="Replies to a specific message.",
)
async def telegram_reply_to_message_impl(
    ctx: Context, args: TelegramReplyToMessageInput
) -> ReplyMessageOutput:
    if error := await _check_client():
        return ReplyMessageOutput(status="failed", error=error.error)
    try:
        result_dict = await client.telegram_wrapper_instance.reply_to_message(
            args.chat_id, args.message_id, args.text
        )
        return ReplyMessageOutput(**result_dict)
    except Exception as e:
        err_out = _handle_error("telegram_reply_to_message", e)
        return ReplyMessageOutput(status="failed", error=err_out.error)


@mcp.tool(
    name="telegram_add_reaction",
    description="Adds an emoji reaction.",
)
async def telegram_add_reaction_impl(
    ctx: Context, args: TelegramAddReactionInput
) -> AddReactionOutput:
    if error := await _check_client():
        return AddReactionOutput(status="failed", error=error.error)
    try:
        result_dict = await client.telegram_wrapper_instance.add_reaction(
            args.chat_id, args.message_id, args.reaction
        )
        return AddReactionOutput(**result_dict)
    except Exception as e:
        err_out = _handle_error("telegram_add_reaction", e)
        return AddReactionOutput(status="failed", error=err_out.error)


@mcp.tool(
    name="telegram_get_chat_history",
    description="Retrieves recent messages.",
)
async def telegram_get_chat_history_impl(
    ctx: Context, args: TelegramGetChatHistoryInput
) -> MaybeErrorList:
    if error := await _check_client():
        return error
    try:
        messages = await client.telegram_wrapper_instance.get_chat_history(
            args.chat_id, args.limit, args.max_id
        )
        return messages
    except Exception as e:
        return _handle_error("telegram_get_chat_history", e)


@mcp.tool(
    name="telegram_get_user_profile",
    description="Retrieves user profile information.",
)
async def telegram_get_user_profile_impl(
    ctx: Context, args: TelegramGetUserProfileInput
) -> MaybeErrorDict:
    if error := await _check_client():
        return error
    try:
        profile = await client.telegram_wrapper_instance.get_user_profile(args.user_id)
        if isinstance(profile, dict) and "error" in profile:
            return ErrorOutput(error=profile["error"])
        return profile
    except Exception as e:
        return _handle_error("telegram_get_user_profile", e)


@mcp.tool(
    name="search_telegram_messages",
    description="Searches messages globally or within a specific chat using the Telegram API.",
)
async def search_telegram_messages_impl(
    ctx: Context, args: TelegramSearchMessagesInput
) -> MaybeErrorList:
    if error := await _check_client():
        return error
    try:
        results = await client.telegram_wrapper_instance.search_messages(
            query=args.query, chat_id=args.chat_id, limit=args.limit
        )
        return results
    except Exception as e:
        return _handle_error("search_telegram_messages", e)
