import logging
from contextlib import asynccontextmanager
from typing import Optional, AsyncGenerator, Any

from mcp.server.fastmcp import FastMCP, Context  # Import Context

# Import necessary components from other modules
from .client import TelegramClientWrapper
from .schemas import ErrorOutput
from . import tools  # Import the tools module

logger = logging.getLogger(__name__)

# --- Global Client Instance ---
# This instance is managed by the lifespan function
# We don't strictly need this global anymore if accessed via app.state
# telegram_wrapper_instance: Optional[TelegramClientWrapper] = None

# --- Lifespan Management ---


@asynccontextmanager
async def lifespan(
    app: FastMCP,
) -> AsyncGenerator[None, None]:  # Yield None, state is attached to app
    """Manages the Telegram client connection lifecycle for the running server."""
    # global telegram_wrapper_instance # No longer need global if using app.state
    logger.info("MCP Server lifespan starting...")
    wrapper = TelegramClientWrapper()
    app.state.tg_client = None  # Initialize state attribute
    try:
        logger.info("Connecting Telegram client using existing session...")
        connected = await wrapper.connect(perform_login_if_needed=False)
        if connected:
            # telegram_wrapper_instance = wrapper # Store on app state instead
            app.state.tg_client = wrapper
            logger.info("Telegram client connected and authorized via session.")
        else:
            logger.warning(
                "Lifespan: Failed to connect/authorize using session. Tools requiring auth will fail."
            )
            # Still store the wrapper instance on state, even if not authorized
            # Tools can check authorization status via the instance.
            app.state.tg_client = wrapper

        yield  # Lifespan yields control to the running server

    except Exception as e:
        logger.error(f"FATAL: Exception during lifespan connection: {e}", exc_info=True)
        app.state.tg_client = None  # Ensure state is None on error
        # Re-raise the exception to potentially stop server startup if critical
        raise
    finally:
        logger.info("MCP Server lifespan ending...")
        client_instance = getattr(app.state, "tg_client", None)
        if client_instance:
            logger.info("Disconnecting client during lifespan shutdown...")
            await client_instance.disconnect()
            app.state.tg_client = None  # Clear state


# --- FastMCP Server Instance ---
mcp = FastMCP(lifespan=lifespan)


# --- Helper Functions ---


def _handle_error(tool_name: str, e: Exception) -> ErrorOutput:
    """Logs an error and returns a formatted ErrorOutput."""
    logger.error(f"Error in {tool_name} tool: {e}", exc_info=True)
    return ErrorOutput(error=f"An unexpected error occurred in {tool_name}: {str(e)}")


# Modify _check_client to use the context to get the client instance
def _check_client(ctx: Context) -> Optional[ErrorOutput]:
    """Checks if the client instance is available and connected via context state."""
    client_instance: Optional[TelegramClientWrapper] = getattr(
        ctx.app.state, "tg_client", None
    )

    if not client_instance:
        return ErrorOutput(
            error="Telegram client wrapper not initialized. Lifespan may have failed."
        )
    if not client_instance.client or not client_instance.client.is_connected():
        return ErrorOutput(
            error="Telegram client is not connected. Check server logs or restart."
        )
    # We also need to check authorization for most operations
    # Let's add a check here, assuming most tools need it.
    # Specific tools that *don't* need auth (like login_status) can skip this check.
    # Note: This requires is_user_authorized to be synchronous or handled carefully.
    # Telethon's is_user_authorized is async, so this check cannot be done synchronously here.
    # The check must happen within the async tool implementation itself.
    # We'll rely on the tool calling client_instance._ensure_connected() which is async.

    return None


# --- Tool Registration ---
# Import implementations from tools.py and register them with the MCP instance

# Pass the helper functions to the tools module if needed, or have tools import them directly
# For simplicity, let tools import _handle_error directly. _check_client is now internal to tools.


@mcp.tool(
    name="telegram_login_status",
    description="Checks the current connection and authorization status.",
)
async def telegram_login_status(*args: Any, **kwargs: Any) -> Any:
    # Pass through arguments and context to the implementation
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
