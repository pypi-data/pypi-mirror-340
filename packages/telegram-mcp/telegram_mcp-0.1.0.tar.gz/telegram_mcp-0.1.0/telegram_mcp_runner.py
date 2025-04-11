# Note: Dependencies are now managed in pyproject.toml

import asyncio
import argparse
import logging
import os
import sys  # Ensure sys is imported
import json  # Added
import webbrowser
from contextlib import asynccontextmanager
from typing import AsyncGenerator, List, Dict, Optional, Union, Any  # Removed Callable
from pathlib import Path  # Ensure Path is imported

# Third-party Libraries
import qrcode
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.types import Message, User, Chat, Channel
from pydantic import BaseModel, Field
from mcp.server.fastmcp import FastMCP, Context  # Correct import path for Context

# --- Configuration ---

# Use hardcoded keys as fallback if environment variables are not set
DEFAULT_API_ID = 611335
DEFAULT_API_HASH = "d524b414d21f4d37f08684c1df41ac9c"
# THIS_SCRIPT_GITHUB_URL removed, will be determined dynamically during install

# Standard data directory in user's home
DATA_DIR_NAME = ".telegram_mcp_data"
HOME_DATA_DIR = Path.home() / DATA_DIR_NAME
SESSION_FILENAME = "telegram.session"
QR_CODE_FILENAME = "login_qr.png"

# Cursor config constants removed - manual configuration required after install
# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],  # Log to stdout for uv run visibility
)
logger = logging.getLogger("TelegramMCPRunner")  # Ensure logger is defined early
logger = logging.getLogger("TelegramMCPRunner")

# --- Pydantic Schemas (Combined from schemas.py) ---


class TelegramListChatsInput(BaseModel):
    limit: int = Field(
        default=100, description="Maximum number of chats to retrieve", ge=1, le=1000
    )


class TelegramSearchChatsInput(BaseModel):
    query: str = Field(..., description="Query string to search for chat/user names")


class TelegramPostMessageInput(BaseModel):
    chat_id: int | str = Field(..., description="Target chat ID or username")
    text: str = Field(..., description="Message text to send")


class TelegramReplyToMessageInput(BaseModel):
    chat_id: int | str = Field(..., description="Target chat ID or username")
    message_id: int = Field(..., description="The ID of the message to reply to")
    text: str = Field(..., description="Reply text")


class TelegramAddReactionInput(BaseModel):
    chat_id: int | str = Field(..., description="Target chat ID or username")
    message_id: int = Field(..., description="The ID of the message to react to")
    reaction: str = Field(..., description="Single emoji character for the reaction")


class TelegramGetChatHistoryInput(BaseModel):
    chat_id: int | str = Field(..., description="Target chat ID or username")
    limit: int = Field(
        default=20, description="Maximum number of messages to retrieve", ge=1, le=100
    )
    max_id: Optional[int] = Field(
        default=None, description="Retrieve messages older than this message ID"
    )


class TelegramSearchMessagesInput(BaseModel):
    query: str = Field(..., description="The text content to search for in messages")
    chat_id: Optional[Union[int, str]] = Field(
        default=None,
        description="Optional chat ID or username to limit the search to a specific chat. Searches globally if None.",
    )
    limit: int = Field(
        default=20, description="Maximum number of messages to return", ge=1, le=100
    )


class TelegramGetUserProfileInput(BaseModel):
    user_id: int | str = Field(..., description="The ID or username of the user")


class LoginStatusUserOutput(BaseModel):
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]


class LoginStatusOutput(BaseModel):
    connected: bool
    authorized: bool
    message: Optional[str] = None
    user: Optional[LoginStatusUserOutput] = None


class StatusOutput(BaseModel):
    status: str = Field(..., description="'success' or 'failed'")
    error: Optional[str] = Field(
        default=None, description="Error message if status is 'failed'"
    )


class PostMessageOutput(StatusOutput):
    message_id: Optional[int] = None
    timestamp: Optional[str] = None


class ReplyMessageOutput(PostMessageOutput):
    pass


class AddReactionOutput(StatusOutput):
    pass


class UserProfileOutput(BaseModel):
    id: int
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]
    phone: Optional[str]
    is_bot: bool
    is_contact: bool
    is_mutual_contact: bool
    status: Optional[str]


class ErrorOutput(BaseModel):
    error: str


MaybeErrorList = List[Dict[str, Any]] | ErrorOutput
MaybeErrorDict = Dict[str, Any] | ErrorOutput

# --- Telegram Client Wrapper (Combined from telegram_client.py) ---


class TelegramClientWrapper:
    """Wraps the Telethon client for easier use within the MCP server."""

    def __init__(self):
        # Load optional overrides from .env in CWD if it exists
        load_dotenv(dotenv_path=Path.cwd() / ".env")

        self.api_id: int = int(os.getenv("TG_API_ID", DEFAULT_API_ID))
        self.api_hash: str = os.getenv("TG_API_HASH", DEFAULT_API_HASH)
        self.phone_number: Optional[str] = os.getenv(
            "TG_PHONE_NUMBER"
        )  # Only for potential 2FA prompt clarity

        self.session_path: Path = HOME_DATA_DIR / SESSION_FILENAME
        self.qr_code_path: Path = HOME_DATA_DIR / QR_CODE_FILENAME

        self.client: Optional[TelegramClient] = None
        HOME_DATA_DIR.mkdir(exist_ok=True)  # Ensure data directory exists
        logger.info(
            f"TelegramClientWrapper initialized. Session path: {self.session_path}"
        )

    async def connect(self, perform_login_if_needed: bool = False) -> bool:
        """
        Initializes and connects the Telethon client.
        If perform_login_if_needed is True, attempts QR login if not authorized.
        Returns True if connected and authorized, False otherwise (or raises error on login failure).
        """
        if self.client and self.client.is_connected():
            logger.info("Client already connected.")
            try:
                if await self.client.is_user_authorized():
                    logger.info("User already authorized.")
                    return True
                else:
                    logger.warning("Client connected but user not authorized.")
                    if perform_login_if_needed:
                        return await self._perform_qr_login()
                    else:
                        return (
                            False  # Connected but not authorized, login not requested
                        )
            except Exception as e:
                logger.error(f"Error checking authorization status: {e}")
                await self.disconnect()  # Disconnect if check fails
                return False

        logger.info(f"Initializing TelegramClient with session: {self.session_path}")
        self.client = TelegramClient(
            str(self.session_path),
            self.api_id,
            self.api_hash,
            system_version="4.16.30-vxCUSTOM",  # Recommended by Telethon docs
        )

        try:
            logger.info("Connecting to Telegram...")
            await self.client.connect()
            logger.info("Initial connection successful.")

            if await self.client.is_user_authorized():
                user = await self.client.get_me()
                logger.info(f"User {user.username or user.id} is authorized.")
                return True
            else:
                logger.warning("User is not authorized.")
                if perform_login_if_needed:
                    return await self._perform_qr_login()
                else:
                    # Not authorized, and login not requested by caller
                    await self.disconnect()  # Disconnect if not proceeding to login
                    return False

        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            await self.disconnect()  # Ensure cleanup on failure
            # If login was requested, re-raise; otherwise, just return False
            if perform_login_if_needed:
                raise
            else:
                return False

    async def _perform_qr_login(self) -> bool:
        """Handles the blocking QR code login flow."""
        if not self.client or not self.client.is_connected():
            logger.error("Cannot perform QR login, client not connected.")
            return False

        logger.warning("Initiating QR code login...")
        qr_login_data = None
        try:
            # Start QR login - this returns immediately with URL, then waits internally
            qr_login_data = await self.client.qr_login()
            logger.info(f"QR Login URL generated: {qr_login_data.url}")

            # Generate QR code image
            qr_img = qrcode.make(qr_login_data.url)
            qr_img.save(str(self.qr_code_path))
            logger.info(f"QR code saved to {self.qr_code_path}")

            # Open QR code in browser (with fallback instructions)
            opened_browser = False
            try:
                opened_browser = webbrowser.open(
                    f"file://{self.qr_code_path.resolve()}"
                )
                if opened_browser:
                    logger.info("Attempted to open QR code in default web browser.")
                else:
                    logger.warning(
                        "webbrowser.open() returned False. Browser might not have opened."
                    )
            except Exception as wb_err:
                logger.error(
                    f"Could not open QR code in browser automatically: {wb_err}"
                )

            # Print instructions regardless of browser opening success
            print("\n" + "=" * 60)
            print(" ACTION REQUIRED: Login to Telegram ".center(60, "="))
            print("=" * 60)
            if opened_browser:
                print("A QR code should have opened in your web browser.")
            else:
                print("Could not open QR code automatically.")
            print(f"Please manually open the file: {self.qr_code_path.resolve()}")
            print("Then scan it using your Telegram app:")
            print("  Settings > Devices > Link Desktop Device")
            print("\nThe script will wait for you to complete the login...")
            print("=" * 60 + "\n")

            # qr_login() waits internally for the scan.
            # The initial call already started the wait. We just need to let it complete.
            # Add a small delay to allow authorization to propagate
            await asyncio.sleep(2)
            # Re-fetch the user after potential login to confirm success
            # Re-fetch the user after potential login to confirm success
            user = await self.client.get_me()
            if user:
                logger.info(f"QR Login successful for user: {user.username or user.id}")
                return True  # Login succeeded
            else:
                # Handle case where get_me() returns None after qr_login
                logger.error(
                    "QR Login failed: Could not retrieve user info after scan."
                )
                return False  # Indicate login failure

        except SessionPasswordNeededError:
            logger.warning("Two-factor authentication enabled after QR scan.")
            # IMPORTANT: This still requires manual input in the terminal
            try:
                # Use getpass for slightly better password handling if available? No, stick to input for simplicity.
                password = input("Enter your Telegram password (2FA): ")
                await self.client.sign_in(password=password)
                logger.info("Sign in with password successful.")
                return True  # Login succeeded
            except Exception as pwd_err:
                logger.error(f"Password sign in failed: {pwd_err}")
                await self.disconnect()  # Disconnect on failure
                return False  # Login failed
        except Exception as qr_err:
            logger.error(f"QR Login process failed: {qr_err}")
            await self.disconnect()  # Disconnect on failure
            return False  # Login failed
        finally:
            # Clean up QR code image file
            if self.qr_code_path.exists():
                try:
                    os.remove(self.qr_code_path)
                    logger.info("Removed temporary QR code image.")
                except OSError as rm_err:
                    logger.warning(
                        f"Could not remove QR code image {self.qr_code_path}: {rm_err}"
                    )

    async def disconnect(self):
        """Disconnects the Telethon client if connected."""
        if self.client and self.client.is_connected():
            logger.info("Disconnecting Telegram client...")
            await self.client.disconnect()
            logger.info("Client disconnected.")
        self.client = None

    async def _ensure_connected(self):
        """Checks if the client is connected and authorized, raises error if not."""
        if not self.client or not self.client.is_connected():
            raise ConnectionError(
                "Telegram client is not connected. Please restart the server or check logs."
            )
        if not await self.client.is_user_authorized():
            raise ConnectionError(
                "Telegram client is connected but not authorized. Session might be invalid. Please restart the server."
            )

    async def get_login_status(self) -> Dict[str, Any]:
        """Checks the connection and authorization status."""
        if not self.client:
            return {
                "connected": False,
                "authorized": False,
                "message": "Client not initialized.",
            }

        connected = False
        authorized = False
        user_info = None
        message = "Status check failed."

        try:
            connected = self.client.is_connected()
            if connected:
                authorized = await self.client.is_user_authorized()
                if authorized:
                    me = await self.client.get_me()
                    user_info = {
                        "id": me.id,
                        "username": me.username,
                        "first_name": me.first_name,
                        "last_name": me.last_name,
                    }
                    message = "Client connected and authorized."
                else:
                    message = "Client connected but not authorized. Login may be required (restart server)."
            else:
                message = "Client not connected."
        except Exception as e:
            logger.warning(
                f"Error checking authorization status during status check: {e}"
            )
            message = f"Error checking status: {str(e)}"
            connected = self.client.is_connected()  # Re-check basic connection
            authorized = False
            user_info = None

        status = {"connected": connected, "authorized": authorized, "message": message}
        if user_info:
            status["user"] = user_info
        return status

    # --- Wrapper Methods for Tools ---

    async def list_chats(self, limit: int = 100) -> List[Dict]:
        await self._ensure_connected()
        logger.info(f"Listing up to {limit} dialogs...")
        dialogs_data = []
        try:
            async for dialog in self.client.iter_dialogs(limit=limit):
                entity = dialog.entity
                entity_type = "Unknown"
                if isinstance(entity, User):
                    entity_type = "User"
                elif isinstance(entity, Chat):
                    entity_type = "Group"
                elif isinstance(entity, Channel):
                    entity_type = "Channel" if entity.broadcast else "Supergroup"

                dialogs_data.append(
                    {
                        "id": dialog.id,
                        "name": dialog.name,
                        "type": entity_type,
                        "unread_count": dialog.unread_count,
                    }
                )
            logger.info(f"Retrieved {len(dialogs_data)} dialogs.")
            return dialogs_data
        except Exception as e:
            logger.error(f"Failed to list chats: {e}", exc_info=True)
            return [{"error": f"Failed to list chats: {str(e)}"}]

    async def search_chats(self, query: str) -> List[Dict]:
        await self._ensure_connected()
        logger.info(f"Searching for chats/users matching query: '{query}'")
        results = []
        query_lower = query.lower()
        try:
            async for dialog in self.client.iter_dialogs():
                if dialog.name and query_lower in dialog.name.lower():
                    entity = dialog.entity
                    entity_type = "Unknown"
                    if isinstance(entity, User):
                        entity_type = "User"
                    elif isinstance(entity, Chat):
                        entity_type = "Group"
                    elif isinstance(entity, Channel):
                        entity_type = "Channel" if entity.broadcast else "Supergroup"
                    results.append(
                        {"id": dialog.id, "name": dialog.name, "type": entity_type}
                    )
            logger.info(f"Found {len(results)} chats/users matching query.")
            return results
        except Exception as e:
            logger.error(f"Failed during chat search: {e}", exc_info=True)
            return [{"error": f"Failed during chat search: {str(e)}"}]

    async def post_message(self, chat_id: Union[int, str], text: str) -> Dict:
        await self._ensure_connected()
        logger.info(f"Sending message to chat_id {chat_id}")
        try:
            message: Message = await self.client.send_message(chat_id, text)
            logger.info(f"Message sent successfully. ID: {message.id}")
            return {
                "message_id": message.id,
                "status": "success",
                "timestamp": message.date.isoformat(),
            }
        except Exception as e:
            logger.error(f"Failed to send message to {chat_id}: {e}", exc_info=True)
            return {"error": str(e), "status": "failed"}

    async def reply_to_message(
        self, chat_id: Union[int, str], message_id: int, text: str
    ) -> Dict:
        await self._ensure_connected()
        logger.info(f"Replying to message ID {message_id} in chat_id {chat_id}")
        try:
            message: Message = await self.client.send_message(
                chat_id, text, reply_to=message_id
            )
            logger.info(f"Reply sent successfully. ID: {message.id}")
            return {
                "message_id": message.id,
                "status": "success",
                "timestamp": message.date.isoformat(),
            }
        except Exception as e:
            logger.error(
                f"Failed to reply to message {message_id} in {chat_id}: {e}",
                exc_info=True,
            )
            return {"error": str(e), "status": "failed"}

    async def add_reaction(
        self, chat_id: Union[int, str], message_id: int, reaction: str
    ) -> Dict:
        await self._ensure_connected()
        logger.info(
            f"Adding reaction '{reaction}' to message ID {message_id} in chat_id {chat_id}"
        )
        try:
            await self.client.send_reaction(chat_id, message_id, reaction=reaction)
            logger.info(f"Reaction '{reaction}' added successfully.")
            return {"status": "success"}
        except Exception as e:
            logger.error(
                f"Failed to add reaction to message {message_id} in {chat_id}: {e}",
                exc_info=True,
            )
            return {"error": str(e), "status": "failed"}

    async def get_chat_history(
        self, chat_id: Union[int, str], limit: int, max_id: Optional[int]
    ) -> List[Dict]:
        await self._ensure_connected()
        logger.info(
            f"Getting {limit} messages from chat_id {chat_id}, ending before ID {max_id or 'latest'}"
        )
        messages_data = []
        try:
            async for message in self.client.iter_messages(
                entity=chat_id, limit=limit, max_id=max_id or 0
            ):
                if isinstance(message, Message):
                    sender_info = {"id": message.sender_id}  # Basic info
                    messages_data.append(
                        {
                            "id": message.id,
                            "text": message.text
                            or f"[Non-text content: {type(message.media).__name__ if message.media else 'None'}]",
                            "sender": sender_info,
                            "timestamp": message.date.isoformat(),
                            "is_reply": message.is_reply,
                            "reply_to_msg_id": message.reply_to_msg_id
                            if message.is_reply
                            else None,
                            "is_outgoing": message.out,
                        }
                    )
            logger.info(f"Retrieved {len(messages_data)} messages.")
            return messages_data
        except Exception as e:
            logger.error(f"Failed to get messages from {chat_id}: {e}", exc_info=True)
            return [{"error": f"Failed to get messages: {str(e)}"}]

    async def get_user_profile(self, user_id: Union[int, str]) -> Dict:
        await self._ensure_connected()
        logger.info(f"Getting profile for user_id: {user_id}")
        try:
            entity = await self.client.get_entity(user_id)
            if isinstance(entity, User):
                profile_data = {
                    "id": entity.id,
                    "username": entity.username,
                    "first_name": entity.first_name,
                    "last_name": entity.last_name,
                    "phone": entity.phone,
                    "is_bot": entity.bot,
                    "is_contact": entity.contact,
                    "is_mutual_contact": entity.mutual_contact,
                    "status": str(entity.status) if entity.status else None,
                }
                logger.info(
                    f"Retrieved profile for user {entity.username or entity.id}"
                )
                return profile_data
            else:
                logger.warning(
                    f"Entity found for {user_id} is not a User (type: {type(entity).__name__})"
                )
                return {"error": f"ID {user_id} does not correspond to a user."}
        except ValueError:
            logger.error(f"Could not find entity for user_id: {user_id}")
            return {
                "error": f"User with ID/username '{user_id}' not found or inaccessible."
            }
        except Exception as e:
            logger.error(
                f"Failed to get user profile for {user_id}: {e}", exc_info=True
            )
            return {"error": f"An error occurred while fetching profile: {str(e)}"}

    async def search_messages(
        self, query: str, chat_id: Optional[Union[int, str]] = None, limit: int = 20
    ) -> List[Dict]:
        """Searches for messages containing the query text, globally or in a specific chat."""
        await self._ensure_connected()
        search_scope = f"chat_id {chat_id}" if chat_id else "globally"
        logger.info(
            f"Searching up to {limit} messages {search_scope} for query: '{query}'"
        )
        messages_data = []
        try:
            # Determine the entity to search within
            entity = None
            if chat_id:
                try:
                    entity = await self.client.get_entity(chat_id)
                except ValueError:
                    logger.error(f"Could not find entity for chat_id: {chat_id}")
                    return [
                        {
                            "error": f"Chat/User with ID/username '{chat_id}' not found or inaccessible."
                        }
                    ]
                except Exception as e:
                    logger.error(
                        f"Error resolving entity for chat_id {chat_id}: {e}",
                        exc_info=True,
                    )
                    return [{"error": f"Error resolving entity {chat_id}: {str(e)}"}]

            async for message in self.client.iter_messages(
                entity=entity,  # None searches globally (within indexed messages)
                limit=limit,
                search=query,
                # filter=InputMessagesFilterEmpty() # Use this if searching ALL messages globally is needed, might be slow/heavy
            ):
                if isinstance(message, Message):
                    # Basic sender info, avoid fetching full entity for performance
                    sender_info = {"id": message.sender_id}
                    messages_data.append(
                        {
                            "id": message.id,
                            "chat_id": message.chat_id,  # Use chat_id directly
                            "text": message.text
                            or f"[Non-text content: {type(message.media).__name__ if message.media else 'None'}]",
                            "sender": sender_info,
                            "timestamp": message.date.isoformat(),
                            "is_reply": message.is_reply,
                            "reply_to_msg_id": message.reply_to_msg_id
                            if message.is_reply
                            else None,
                            "is_outgoing": message.out,
                        }
                    )
            logger.info(f"Retrieved {len(messages_data)} messages matching query.")
            return messages_data
        except Exception as e:
            logger.error(
                f"Failed to search messages ({search_scope}): {e}", exc_info=True
            )


# --- Function to Update Cursor Config ---
def update_cursor_config() -> bool:
    """Reads, updates, and writes the Cursor MCP configuration file."""
    cursor_config_path = Path.home() / ".cursor" / "mcp.json"
    server_config = {
        "name": "telegram-mcp",
        "command": ["telegram-mcp"],  # Use the installed command
        "type": "stdio",
        "description": "Interact with Telegram via MCP",
    }
    config_data = {"servers": []}  # Default structure

    try:
        # Ensure parent directory exists
        cursor_config_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Ensured directory exists: {cursor_config_path.parent}")

        # Read existing config
        if cursor_config_path.exists():
            logger.info(f"Reading existing Cursor config: {cursor_config_path}")
            with open(cursor_config_path, "r") as f:
                try:
                    existing_data = json.load(f)
                    # Validate basic structure
                    if isinstance(existing_data, dict) and isinstance(
                        existing_data.get("servers"), list
                    ):
                        config_data = existing_data
                        logger.info("Successfully loaded existing config.")
                    else:
                        logger.warning(
                            f"Existing config file {cursor_config_path} has invalid structure. Re-initializing."
                        )
                except json.JSONDecodeError:
                    logger.warning(
                        f"Existing config file {cursor_config_path} is not valid JSON. Re-initializing."
                    )
        else:
            logger.info(
                f"Cursor config file not found at {cursor_config_path}. Creating new one."
            )

        # Update config data
        server_exists = False
        for i, server in enumerate(config_data.get("servers", [])):
            if isinstance(server, dict) and server.get("name") == server_config["name"]:
                logger.info(
                    f"Updating existing server entry for '{server_config['name']}'."
                )
                config_data["servers"][i] = server_config
                server_exists = True
                break

        if not server_exists:
            logger.info(f"Adding new server entry for '{server_config['name']}'.")
            # Ensure 'servers' key exists and is a list
            if not isinstance(config_data.get("servers"), list):
                config_data["servers"] = []
            config_data["servers"].append(server_config)

        # Write updated config
        logger.info(f"Writing updated config to {cursor_config_path}")
        with open(cursor_config_path, "w") as f:
            json.dump(config_data, f, indent=2)
        logger.info("Successfully updated Cursor MCP configuration.")
        return True

    except (IOError, OSError) as e:
        logger.error(
            f"Failed to write Cursor config file {cursor_config_path}: {e}",
            exc_info=True,
        )
        return False
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during Cursor config update: {e}",
            exc_info=True,
        )
        return False


# --- MCP Server Setup (Combined from server.py) ---

telegram_wrapper_instance: Optional[TelegramClientWrapper] = None


@asynccontextmanager
async def lifespan(
    app: FastMCP,
) -> AsyncGenerator[Optional[TelegramClientWrapper], None]:
    """Manages the Telegram client connection lifecycle for the running server."""
    global telegram_wrapper_instance
    if telegram_wrapper_instance is None:
        logger.info("MCP Server lifespan starting...")
        wrapper = TelegramClientWrapper()
        try:
            # init_db() # Removed database initialization
            logger.info("Connecting Telegram client using existing session...")
            connected = await wrapper.connect(perform_login_if_needed=False)
            if connected:
                telegram_wrapper_instance = wrapper
                logger.info("Telegram client connected and authorized via session.")
                yield wrapper
            else:
                logger.error(
                    "Lifespan: Failed to connect/authorize using session. Server tools will be unavailable."
                )
                telegram_wrapper_instance = None
                yield None
        except Exception as e:
            logger.error(
                f"FATAL: Exception during lifespan connection: {e}", exc_info=True
            )
            telegram_wrapper_instance = None
            yield None
        # No finally block needed here, disconnect happens on server shutdown via main block
    else:
        logger.warning("Lifespan entered but telegram_wrapper_instance already exists.")
        yield telegram_wrapper_instance


mcp = FastMCP(lifespan=lifespan)


# --- Helper Function for Error Handling ---
def _handle_error(tool_name: str, e: Exception) -> ErrorOutput:
    logger.error(f"Error in {tool_name} tool: {e}", exc_info=True)
    return ErrorOutput(error=f"An unexpected error occurred in {tool_name}: {str(e)}")


def _check_client() -> Optional[ErrorOutput]:
    """Checks if the client is available, returns error dict if not."""
    if (
        not telegram_wrapper_instance
        or not telegram_wrapper_instance.client
        or not telegram_wrapper_instance.client.is_connected()
    ):
        return ErrorOutput(
            error="Telegram client is not connected or authorized. Check server logs or restart."
        )
    # Authorization check is implicitly handled by _ensure_connected in wrapper methods
    return None


# --- MCP Tools (Combined from server.py) ---


@mcp.tool(
    name="telegram_login_status",
    description="Checks the current connection and authorization status.",
)
async def telegram_login_status(
    ctx: Context,  # Added Context type hint
) -> LoginStatusOutput:  # Removed ToolContext type hint
    checker = telegram_wrapper_instance or TelegramClientWrapper()
    try:
        status = await checker.get_login_status()
        # Ensure the return type matches LoginStatusOutput schema
        return LoginStatusOutput(**status)
    except Exception as e:
        logger.error(f"Error getting login status via tool: {e}", exc_info=True)
        return LoginStatusOutput(
            connected=False,
            authorized=False,
            message=f"Error checking status: {str(e)}",
        )


@mcp.tool(
    name="telegram_list_chats",
    description="Lists recent chats, channels, and conversations.",
    # input_schema removed, inferred from type hints
)
async def telegram_list_chats(  # Added Context type hint
    ctx: Context, args: TelegramListChatsInput
) -> MaybeErrorList:
    if error := _check_client():
        return error
    try:
        results = await telegram_wrapper_instance.list_chats(
            limit=args.limit
        )  # Access limit from args
        if isinstance(results, list) and results and "error" in results[0]:
            return ErrorOutput(error=results[0]["error"])
        return results
    except Exception as e:
        return _handle_error("telegram_list_chats", e)


@mcp.tool(
    name="telegram_search_chats",
    description="Searches chats, channels, or users by name.",
    # input_schema removed, inferred from type hints
)
async def telegram_search_chats(  # Added Context type hint
    ctx: Context, args: TelegramSearchChatsInput
) -> MaybeErrorList:
    if error := _check_client():
        return error
    try:
        results = await telegram_wrapper_instance.search_chats(
            args.query
        )  # Use args.query
        if isinstance(results, list) and results and "error" in results[0]:
            return ErrorOutput(error=results[0]["error"])
        return results
    except Exception as e:
        return _handle_error("telegram_search_chats", e)


@mcp.tool(  # Removed input_schema
    name="telegram_post_message",
    description="Sends a text message.",
)
async def telegram_post_message(
    ctx: Context,
    args: TelegramPostMessageInput,  # Added Context type hint
) -> PostMessageOutput:  # Changed signature
    if error := _check_client():
        return error
    try:
        result = await telegram_wrapper_instance.post_message(
            args.chat_id, args.text
        )  # Use args
        return PostMessageOutput(**result)
    except Exception as e:
        return _handle_error("telegram_post_message", e)


@mcp.tool(  # Removed input_schema
    name="telegram_reply_to_message",
    description="Replies to a specific message.",
)
async def telegram_reply_to_message(
    ctx: Context,
    args: TelegramReplyToMessageInput,  # Added Context type hint
) -> ReplyMessageOutput:  # Changed signature
    if error := _check_client():
        return error
    try:
        result = await telegram_wrapper_instance.reply_to_message(  # Use args
            args.chat_id, args.message_id, args.text
        )
        return ReplyMessageOutput(**result)
    except Exception as e:
        return _handle_error("telegram_reply_to_message", e)


@mcp.tool(  # Removed input_schema
    name="telegram_add_reaction",
    description="Adds an emoji reaction.",
)
async def telegram_add_reaction(
    ctx: Context,
    args: TelegramAddReactionInput,  # Added Context type hint
) -> AddReactionOutput:  # Changed signature
    if error := _check_client():
        return error
    try:
        result = await telegram_wrapper_instance.add_reaction(  # Use args
            args.chat_id, args.message_id, args.reaction
        )
        return AddReactionOutput(**result)
    except Exception as e:
        return _handle_error("telegram_add_reaction", e)


@mcp.tool(  # Removed input_schema
    name="telegram_get_chat_history",
    description="Retrieves recent messages.",
)
async def telegram_get_chat_history(
    ctx: Context,
    args: TelegramGetChatHistoryInput,  # Added Context type hint
) -> MaybeErrorList:  # Changed signature
    if error := _check_client():
        return error
    try:
        messages = await telegram_wrapper_instance.get_chat_history(  # Use args
            args.chat_id, args.limit, args.max_id
        )
        if isinstance(messages, list) and messages and "error" in messages[0]:
            return ErrorOutput(error=messages[0]["error"])
        return messages
    except Exception as e:
        return _handle_error("telegram_get_chat_history", e)


@mcp.tool(  # Removed input_schema
    name="telegram_get_user_profile",
    description="Retrieves user profile information.",
)
async def telegram_get_user_profile(
    ctx: Context,
    args: TelegramGetUserProfileInput,  # Added Context type hint
) -> MaybeErrorDict:  # Changed signature
    if error := _check_client():
        return error
    try:
        profile = await telegram_wrapper_instance.get_user_profile(
            args.user_id
        )  # Use args.user_id
        if isinstance(profile, dict) and "error" in profile:
            return ErrorOutput(error=profile["error"])
        # Assuming successful profile is a dict that can be validated by UserProfileOutput if needed
        # For now, return the dict directly as MaybeErrorDict allows Dict[str, Any]
        return profile
    except Exception as e:
        return _handle_error("telegram_get_user_profile", e)


@mcp.tool(  # Removed input_schema
    name="search_telegram_messages",
    description="Searches messages globally or within a specific chat using the Telegram API.",
)
async def search_telegram_messages(
    ctx: Context,
    args: TelegramSearchMessagesInput,  # Added Context type hint
) -> MaybeErrorList:  # Changed signature
    if error := _check_client():
        return error
    try:
        results = await telegram_wrapper_instance.search_messages(  # Use args
            query=args.query, chat_id=args.chat_id, limit=args.limit
        )
        if isinstance(results, list) and results and "error" in results[0]:
            return ErrorOutput(error=results[0]["error"])
        return results
    except Exception as e:
        return _handle_error("search_telegram_messages", e)


# --- Login Function (formerly Installer) ---
# Note: This function now only handles the initial login/session creation.
# Cursor configuration is handled by --install cursor.
async def run_initial_login() -> bool:
    """Performs the initial blocking login to create the session file. Returns True on success, False on failure."""
    print("-" * 60)
    print(" Telegram MCP Server Initial Login ".center(60, "-"))
    print("-" * 60)

    # Script URL determination removed - no longer needed for config update.
    # Cursor config update removed.
    # Perform Login
    print("\nAttempting Telegram login (QR code may open in browser)...")
    # Create a wrapper instance specifically for the install login
    login_wrapper = TelegramClientWrapper()
    login_successful = False
    try:
        # connect() performs the blocking login
        login_successful = await login_wrapper.connect(perform_login_if_needed=True)
        # Explicitly disconnect after successful install login
        if login_wrapper.client and login_wrapper.client.is_connected():
            await login_wrapper.disconnect()
    except Exception as e:
        logger.error(
            f"An unexpected error occurred during install login: {e}", exc_info=True
        )
        login_successful = False
        # Attempt disconnect even on error
        if login_wrapper.client and login_wrapper.client.is_connected():
            try:
                await login_wrapper.disconnect()
            except:
                pass  # Ignore disconnect errors after login error

    print("-" * 60)
    if login_successful:
        print("[SUCCESS] Initial login complete!")
        print(f"Telegram session saved to {login_wrapper.session_path}")
        # Removed manual config instructions
    else:
        print("[FAILURE] Initial login failed.")
        print("Please check the logs above for errors.")
        print(f"Ensure the data directory exists and is writable: {HOME_DATA_DIR}")
    print("-" * 60)
    return login_successful  # Return status instead of exiting


# --- Main Execution Block (Modified) ---
def main():
    """Main function to handle argument parsing and server execution."""
    parser = argparse.ArgumentParser(
        description="Telegram MCP Server Runner / Initial Login / Installation."
    )
    parser.add_argument(
        "--login",
        action="store_true",
        help="Perform the initial login to create the session file (alternative to --install).",
    )
    parser.add_argument(
        "--install",
        type=str,
        metavar="CLIENT_NAME",  # Added metavar for clarity
        help='Install and configure for a specific client (currently only supports "cursor"). Handles login if needed.',
    )
    args = parser.parse_args()

    if args.install:
        client_name = args.install.lower()
        if client_name == "cursor":
            print("\n--- Starting Installation for Cursor ---")

            # 1. Ensure Login
            temp_wrapper = (
                TelegramClientWrapper()
            )  # Use a temporary wrapper to check session path
            if not temp_wrapper.session_path.exists():
                print("Telegram session file not found. Initiating login...")
                login_ok = asyncio.run(run_initial_login())
                if not login_ok:
                    print("[ERROR] Login failed. Cannot proceed with installation.")
                    sys.exit(1)
                print("Login successful.")
            else:
                print(
                    f"Existing session found at {temp_wrapper.session_path}. Skipping login."
                )

            # 2. Update Cursor Config
            print("Updating Cursor MCP configuration...")
            config_updated = update_cursor_config()

            if config_updated:
                print("[SUCCESS] Cursor configuration updated successfully.")
                print(f"Config file: {Path.home() / '.cursor' / 'mcp.json'}")
                print(
                    "\nInstallation complete! Please restart Cursor for changes to take effect."
                )
                print("You can now run the server using: telegram-mcp")
                sys.exit(0)
            else:
                print(
                    "[ERROR] Failed to update Cursor configuration. Check logs above."
                )
                sys.exit(1)

        else:
            print(
                f"[ERROR] Installation currently only supported for 'cursor', not '{args.install}'."
            )
            sys.exit(1)

    elif args.login:
        # Run the initial login process only
        print("Running initial login process only...")
        login_ok = asyncio.run(run_initial_login())
        sys.exit(0 if login_ok else 1)

    else:
        # Default: Start the MCP server
        logger.info("Starting Telegram MCP server...")
        try:
            mcp.run()  # Starts the server and blocks
            logger.info("Telegram MCP server stopped.")
            if telegram_wrapper_instance:
                asyncio.run(telegram_wrapper_instance.disconnect())
        except KeyboardInterrupt:
            logger.info("Server stopped by user (KeyboardInterrupt).")
            if telegram_wrapper_instance:
                asyncio.run(telegram_wrapper_instance.disconnect())
        except Exception as e:
            logger.critical(f"Fatal error running MCP server: {e}", exc_info=True)
            if telegram_wrapper_instance:
                asyncio.run(telegram_wrapper_instance.disconnect())
            sys.exit(1)
        sys.exit(0)


if __name__ == "__main__":
    main()
