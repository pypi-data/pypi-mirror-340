import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any

from mcp.server.fastmcp import FastMCP

# Import necessary components from other modules
# Import the client module to access/update the global instance
from . import client
from . import tools  # Import the tools module

logger = logging.getLogger(__name__)

# --- Global Client Instance ---
# Removed definition from here, it's now in client.py

# --- Lifespan Management ---


@asynccontextmanager
async def lifespan(
    app: FastMCP,
) -> AsyncGenerator[None, None]:
    """Manages the Telegram client connection lifecycle for the running server."""
    # We modify the global instance defined in the client module
    logger.info("MCP Server lifespan starting...")
    if client.telegram_wrapper_instance is not None:
        logger.warning(
            "Lifespan started but telegram_wrapper_instance was not None. Resetting."
        )
        client.telegram_wrapper_instance = None

    # Create a new wrapper instance for this server run
    wrapper = client.TelegramClientWrapper()
    try:
        logger.info("Connecting Telegram client using existing session...")
        connected = await wrapper.connect(perform_login_if_needed=False)
        if connected:
            # Assign the created and connected wrapper to the global in client.py
            client.telegram_wrapper_instance = wrapper
            logger.info("Telegram client connected and authorized via session.")
        else:
            logger.warning(
                "Lifespan: Failed to connect/authorize using session. Tools requiring auth will fail."
            )
            # Store wrapper even if not authorized, tools can check status
            client.telegram_wrapper_instance = wrapper

        yield  # Lifespan yields control

    except Exception as e:
        logger.error(f"FATAL: Exception during lifespan connection: {e}", exc_info=True)
        client.telegram_wrapper_instance = None  # Ensure instance is None on error
        raise
    finally:
        logger.info("MCP Server lifespan ending...")
        # Use the global instance from client module for disconnect
        if client.telegram_wrapper_instance:
            logger.info("Disconnecting client during lifespan shutdown...")
            await client.telegram_wrapper_instance.disconnect()
            client.telegram_wrapper_instance = None  # Clear global instance


# --- FastMCP Server Instance ---
mcp = FastMCP(lifespan=lifespan)


# --- Helper Functions ---
# Removed _handle_error and _check_client from here. They belong in tools.py


# --- Tool Registration ---
# Register tool implementations from tools.py


@mcp.tool(
    name="telegram_login_status",
    description="Checks the current connection and authorization status.",
)
async def telegram_login_status(*args: Any, **kwargs: Any) -> Any:
    return await tools.telegram_login_status_impl(*args, **kwargs)


@mcp.tool(
    name="telegram_list_chats",
    description="Lists recent chats, channels, and conversations.",
)
async def telegram_list_chats(*args: Any, **kwargs: Any) -> Any:
    return await tools.telegram_list_chats_impl(*args, **kwargs)


@mcp.tool(
    name="telegram_search_chats",
    description="Searches chats, channels, or users by name.",
)
async def telegram_search_chats(*args: Any, **kwargs: Any) -> Any:
    return await tools.telegram_search_chats_impl(*args, **kwargs)


@mcp.tool(
    name="telegram_post_message",
    description="Sends a text message.",
)
async def telegram_post_message(*args: Any, **kwargs: Any) -> Any:
    return await tools.telegram_post_message_impl(*args, **kwargs)


@mcp.tool(
    name="telegram_reply_to_message",
    description="Replies to a specific message.",
)
async def telegram_reply_to_message(*args: Any, **kwargs: Any) -> Any:
    return await tools.telegram_reply_to_message_impl(*args, **kwargs)


@mcp.tool(
    name="telegram_add_reaction",
    description="Adds an emoji reaction.",
)
async def telegram_add_reaction(*args: Any, **kwargs: Any) -> Any:
    return await tools.telegram_add_reaction_impl(*args, **kwargs)


@mcp.tool(
    name="telegram_get_chat_history",
    description="Retrieves recent messages.",
)
async def telegram_get_chat_history(*args: Any, **kwargs: Any) -> Any:
    return await tools.telegram_get_chat_history_impl(*args, **kwargs)


@mcp.tool(
    name="telegram_get_user_profile",
    description="Retrieves user profile information.",
)
async def telegram_get_user_profile(*args: Any, **kwargs: Any) -> Any:
    return await tools.telegram_get_user_profile_impl(*args, **kwargs)


@mcp.tool(
    name="search_telegram_messages",
    description="Searches messages globally or within a specific chat using the Telegram API.",
)
async def search_telegram_messages(*args: Any, **kwargs: Any) -> Any:
    return await tools.search_telegram_messages_impl(*args, **kwargs)
