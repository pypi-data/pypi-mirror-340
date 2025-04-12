from pydantic import BaseModel, Field
from typing import Optional, Union, List, Dict, Any

# --- Pydantic Schemas ---


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
