# Telegram MCP Server ✨📲

The simplest MCP server for interacting with Telegram.

## Features 🚀

*   **Easy Setup:** Install and configure for various clients with a single command.
*   **Secure Login:** 
Easy setup with phone number + code flow (supports 2FA). Your session is stored locally.
*   **Core Telegram Actions:** Send messages, list chats, get history, and more via MCP tools.

## Installation & Setup

Requires [`uv`](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer).

1.  **Connect to Telegram:**

    ```bash
    uvx telegram-mcp --login
    ```

    Your session is saved locally to `~/.telegram_mcp_data/telegram.session`.    

2.  **Set up your favorite MCP client:**
    Run the following in your terminal, replacing `<client_key>` with your client (e.g., `cursor`, `vscode`, `cline-cursor`, `cline-vscode`, `windsurf`):
    ```bash
    uvx telegram-mcp --install claude # or vscode, cursor, etc.
    ```

    This command installs the package (if needed) and automatically configures your selected MCP client.

## Available Tools 🛠️

*   `telegram_login_status()`: Check connection/auth status.
*   `telegram_list_chats()`: List recent chats.
*   `telegram_search_chats()`: Find chats/users by name.
*   `telegram_post_message()`: Send a message.
*   `telegram_reply_to_message()`: Reply to a message.
*   `telegram_add_reaction()`: Add an emoji reaction.
*   `telegram_get_chat_history()`: Get recent messages from a chat.
*   `telegram_get_user_profile()`: Get user profile info.
*   `search_telegram_messages()`: Search messages globally or in a chat.

*(Check tool schemas for specific arguments like `chat_id`, `text`, `limit` etc.)*