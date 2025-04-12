import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from mcp.server.fastmcp import FastMCP, Context

# Import necessary components from other modules
from . import client
from . import tools

# Import schemas needed for type hints in registration
from .schemas import (
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


logger = logging.getLogger(__name__)

# --- Global Client Instance ---
# Defined in client.py

# --- Lifespan Management ---


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


# --- FastMCP Server Instance ---
mcp = FastMCP(lifespan=lifespan)


# --- Tool Registration ---
# Signatures now match the implementation functions in tools.py


@mcp.tool(
    name="telegram_login_status",
    description="Checks the current connection and authorization status.",
)
async def telegram_login_status(
    ctx: Context,
) -> LoginStatusOutput:  # Added ctx, specific return type
    # Note: Return type hint helps FastMCP generate schema, but actual return comes from impl
    return await tools.telegram_login_status_impl(ctx)


@mcp.tool(
    name="telegram_list_chats",
    description="Lists recent chats, channels, and conversations.",
)
# Added ctx, args with specific schema type, specific return type
async def telegram_list_chats(
    ctx: Context, args: TelegramListChatsInput
) -> MaybeErrorList:
    return await tools.telegram_list_chats_impl(ctx, args)


@mcp.tool(
    name="telegram_search_chats",
    description="Searches chats, channels, or users by name.",
)
# Added ctx, args with specific schema type, specific return type
async def telegram_search_chats(
    ctx: Context, args: TelegramSearchChatsInput
) -> MaybeErrorList:
    return await tools.telegram_search_chats_impl(ctx, args)


@mcp.tool(
    name="telegram_post_message",
    description="Sends a text message.",
)
# Added ctx, args with specific schema type, specific return type
async def telegram_post_message(
    ctx: Context, args: TelegramPostMessageInput
) -> PostMessageOutput:
    return await tools.telegram_post_message_impl(ctx, args)


@mcp.tool(
    name="telegram_reply_to_message",
    description="Replies to a specific message.",
)
# Added ctx, args with specific schema type, specific return type
async def telegram_reply_to_message(
    ctx: Context, args: TelegramReplyToMessageInput
) -> ReplyMessageOutput:
    return await tools.telegram_reply_to_message_impl(ctx, args)


@mcp.tool(
    name="telegram_add_reaction",
    description="Adds an emoji reaction.",
)
# Added ctx, args with specific schema type, specific return type
async def telegram_add_reaction(
    ctx: Context, args: TelegramAddReactionInput
) -> AddReactionOutput:
    return await tools.telegram_add_reaction_impl(ctx, args)


@mcp.tool(
    name="telegram_get_chat_history",
    description="Retrieves recent messages.",
)
# Added ctx, args with specific schema type, specific return type
async def telegram_get_chat_history(
    ctx: Context, args: TelegramGetChatHistoryInput
) -> MaybeErrorList:
    return await tools.telegram_get_chat_history_impl(ctx, args)


@mcp.tool(
    name="telegram_get_user_profile",
    description="Retrieves user profile information.",
)
# Added ctx, args with specific schema type, specific return type
async def telegram_get_user_profile(
    ctx: Context, args: TelegramGetUserProfileInput
) -> MaybeErrorDict:
    return await tools.telegram_get_user_profile_impl(ctx, args)


@mcp.tool(
    name="search_telegram_messages",
    description="Searches messages globally or within a specific chat using the Telegram API.",
)
# Added ctx, args with specific schema type, specific return type
async def search_telegram_messages(
    ctx: Context, args: TelegramSearchMessagesInput
) -> MaybeErrorList:
    return await tools.search_telegram_messages_impl(ctx, args)
