import json
import logging
import os
import platform
import sys
import tempfile
from pathlib import Path
from typing import List, Dict, Any, Optional, Union

logger = logging.getLogger(__name__)

# --- Configuration Data ---

MCP_CONFIG_DATA = {
    "vscode": {
        "name": "Visual Studio Code",
        "paths": {
            "windows": "%APPDATA%\\Code\\User\\settings.json",
            "osx": "~/Library/Application Support/Code/User/settings.json",
            "linux": "~/.config/Code/User/settings.json",
        },
        "json_path": ["mcp", "servers"],  # Dict target: $.mcp.servers
        "is_dict_target": True,
        "server_name_key": None,
        "template": {
            "command": "uvx",
            "args": ["telegram-mcp"],
            "type": "stdio",
            "description": "Interact with Telegram via MCP (telegram-mcp)",
        },
    },
    "vscode-insiders": {
        "name": "Visual Studio Code Insiders",
        "paths": {
            "windows": "%APPDATA%\\Code - Insiders\\User\\settings.json",
            "osx": "~/Library/Application Support/Code - Insiders/User/settings.json",
            "linux": "~/.config/Code - Insiders/User/settings.json",
        },
        "json_path": ["mcp", "servers"],
        "is_dict_target": True,
        "server_name_key": None,
        "template": {
            "command": "uvx",
            "args": ["telegram-mcp"],
            "type": "stdio",
            "description": "Interact with Telegram via MCP (telegram-mcp)",
        },
    },
    "windsurf": {
        "name": "Windsurf",
        "paths": {
            "windows": "%USERPROFILE%\\.codeium\\windsurf\\mcp_config.json",
            "osx": "~/.codeium/windsurf/mcp_config.json",
            "linux": "~/.codeium/windsurf/mcp_config.json",
        },
        "json_path": ["mcpServers"],  # Dict target: $.mcpServers
        "is_dict_target": True,
        "server_name_key": None,
        "template": {
            "command": "uvx",
            "args": ["telegram-mcp"],
            "type": "stdio",
            "description": "Interact with Telegram via MCP (telegram-mcp)",
        },
    },
    "cursor": {
        "name": "Cursor",
        "paths": {
            "windows": "%USERPROFILE%\\.cursor\\mcp.json",
            "osx": "~/.cursor/mcp.json",
            "linux": "~/.cursor/mcp.json",
        },
        "json_path": ["mcpServers"],  # Dict target: $.mcpServers
        "is_dict_target": True,
        "server_name_key": None,
        "template": {
            "command": "uvx",
            "args": ["telegram-mcp"],
            "type": "stdio",
            "description": "Interact with Telegram via MCP (telegram-mcp)",
        },
    },
    "cline-vscode": {
        "name": "Cline (in VS Code)",
        "paths": {
            "windows": "%APPDATA%\\Code\\User\\globalStorage\\rooveterinaryinc.roo-cline\\settings\\mcp_settings.json",
            "osx": "~/Library/Application Support/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json",
            "linux": "~/.config/Code/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json",
        },
        "json_path": ["mcpServers"],  # Dict target: $.mcpServers
        "is_dict_target": True,
        "server_name_key": None,
        "template": {
            "command": "uvx",
            "args": ["telegram-mcp"],
            "type": "stdio",
            "description": "Interact with Telegram via MCP (telegram-mcp)",
        },
    },
    "cline-cursor": {
        "name": "Cline (in Cursor)",
        "paths": {
            "windows": "%USERPROFILE%\\.cursor\\User\\globalStorage\\rooveterinaryinc.roo-cline\\settings\\mcp_settings.json",
            "osx": "~/Library/Application Support/Cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json",
            "linux": "~/.cursor/User/globalStorage/rooveterinaryinc.roo-cline/settings/mcp_settings.json",
        },
        "json_path": ["mcpServers"],  # Dict target: $.mcpServers
        "is_dict_target": True,
        "server_name_key": None,
        "template": {
            "command": "uvx",
            "args": ["telegram-mcp"],
            "type": "stdio",
            "description": "Interact with Telegram via MCP (telegram-mcp)",
        },
    },
    "claude-desktop": {
        "name": "Claude Desktop",
        "paths": {
            "windows": "%APPDATA%\\Claude\\claude_desktop_config.json",
            "osx": "~/Library/Application Support/Claude/claude_desktop_config.json",
            "linux": "~/.config/Claude/claude_desktop_config.json",
        },
        "json_path": ["mcpServers"],  # Assuming $.mcpServers dict target
        "is_dict_target": True,
        "server_name_key": None,
        "template": {
            "command": "uvx",
            "args": ["telegram-mcp"],
            "type": "stdio",
            "description": "Interact with Telegram via MCP (telegram-mcp)",
        },
    },
    "claude-code": {
        "name": "Claude Code",
        "paths": {
            "windows": "%USERPROFILE%\\.claude.json",
            "osx": "~/.claude.json",
            "linux": "~/.claude.json",
        },
        "json_path": ["mcpServers"],  # Assuming $.mcpServers dict target
        "is_dict_target": True,
        "server_name_key": None,
        "template": {
            "command": "uvx",
            "args": ["telegram-mcp"],
            "type": "stdio",
            "description": "Interact with Telegram via MCP (telegram-mcp)",
        },
    },
}

# --- Helper Functions ---


def get_os_type():
    """Detects the operating system."""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "osx"
    elif system == "linux":
        return "linux"
    else:
        logger.error(f"Unsupported operating system '{platform.system()}'")
        raise OSError(f"Unsupported operating system '{platform.system()}'")


def resolve_path(path_str):
    """Resolves environment variables and ~ in paths."""
    expanded_vars = os.path.expandvars(path_str)
    path = Path(expanded_vars).expanduser()
    return path.resolve()


def load_json_config(file_path: Path) -> Union[Dict, List]:
    """Loads JSON data from a file, returning {} or []. Handles empty/missing files."""
    default_empty: Union[Dict, List] = {}

    if not file_path.exists():
        logger.info(f"Config file '{file_path}' not found. Initializing empty config.")
        return default_empty

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                logger.info(
                    f"Config file '{file_path}' is empty. Initializing empty config."
                )
                return default_empty
            data = json.loads(content)
            if not isinstance(data, (dict, list)):
                logger.warning(
                    f"Config file '{file_path}' root is not a dictionary or list ({type(data)}). Re-initializing."
                )
                return default_empty
            return data
    except json.JSONDecodeError as e:
        logger.error(
            f"Invalid JSON found in '{file_path}'. Please fix or remove the file.",
            exc_info=True,
        )
        raise ValueError(f"Invalid JSON in '{file_path}'") from e
    except Exception as e:
        logger.error(f"Error reading configuration file '{file_path}'", exc_info=True)
        raise IOError(f"Error reading configuration file '{file_path}'") from e


def save_json_config(file_path: Path, data: Union[Dict, List]):
    """Saves JSON data to a file atomically."""
    temp_path = None
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        temp_fd, temp_path_str = tempfile.mkstemp(
            dir=file_path.parent, prefix=file_path.name + "."
        )
        temp_path = Path(temp_path_str)
        with os.fdopen(temp_fd, "w", encoding="utf-8") as f:
            indent = 2 if "settings.json" in file_path.name else 4
            json.dump(data, f, indent=indent)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, file_path)
        logger.info(f"Successfully saved config to {file_path}")
    except Exception as e:
        logger.error(f"Error writing configuration file '{file_path}'", exc_info=True)
        if temp_path and temp_path.exists():
            try:
                temp_path.unlink()
                logger.info(f"Cleaned up temporary file {temp_path}")
            except OSError as unlink_err:
                logger.error(
                    f"Failed to clean up temporary file {temp_path}: {unlink_err}"
                )
        raise IOError(f"Error writing configuration file '{file_path}'") from e


def navigate_and_set(
    config_data: Union[Dict, List],
    path_keys: List[str],
    server_name: str,
    server_config: Dict[str, Any],
    client_key: str,
    is_dict_target: bool,
    server_name_key: Optional[str],
) -> bool:
    """Navigates dict/list using path_keys, sets server_config. Returns True if changes were made."""

    parent_container = config_data
    if not path_keys:
        if is_dict_target and not isinstance(parent_container, dict):
            logger.warning(
                f"Expected root dictionary for {client_key}, found {type(parent_container)}. Re-initializing."
            )
            parent_container = {}
            config_data = parent_container
        elif not is_dict_target and not isinstance(parent_container, list):
            logger.warning(
                f"Expected root list for {client_key}, found {type(parent_container)}. Re-initializing."
            )
            parent_container = []
            config_data = parent_container
    else:
        if not isinstance(config_data, dict):
            logger.warning(
                f"Expected root dictionary for {client_key} to navigate path {path_keys}, found {type(config_data)}. Re-initializing."
            )
            config_data = {}
            parent_container = config_data

        current_level = config_data
        for i, key in enumerate(path_keys):
            is_last_key = i == len(path_keys) - 1
            expected_target_type = dict if is_dict_target else list
            next_level = current_level.get(key)

            if is_last_key:
                if not isinstance(next_level, expected_target_type):
                    logger.warning(
                        f"Creating/resetting target container at key '{key}' for {client_key} as {expected_target_type.__name__}."
                    )
                    next_level = expected_target_type()
                    current_level[key] = next_level
                parent_container = next_level
            else:
                if not isinstance(next_level, dict):
                    logger.warning(
                        f"Creating/resetting intermediate key '{key}' for {client_key} as dict."
                    )
                    next_level = {}
                    current_level[key] = next_level
                current_level = next_level

    made_changes = False
    if is_dict_target:
        if not isinstance(parent_container, dict):
            logger.error(
                f"Internal error: Target container for dict target is not a dict ({type(parent_container)}) for {client_key}."
            )
            raise TypeError("Target container mismatch for dict target")

        existing_server = parent_container.get(server_name)
        if existing_server != server_config:
            action = "Updating" if existing_server else "Adding"
            logger.info(
                f"{action} MCP server '{server_name}' in {client_key} config dict."
            )
            parent_container[server_name] = server_config
            made_changes = True
        else:
            logger.info(
                f"MCP server '{server_name}' already configured identically in {client_key} config dict."
            )

    else:  # Target container is a List
        if not isinstance(parent_container, list):
            logger.error(
                f"Internal error: Target container for list target is not a list ({type(parent_container)}) for {client_key}."
            )
            raise TypeError("Target container mismatch for list target")
        if not server_name_key:
            logger.error(
                f"Internal error: server_name_key not defined for list target client {client_key}."
            )
            raise ValueError("server_name_key missing for list target")

        found_index = -1
        for i, existing_server in enumerate(parent_container):
            if (
                isinstance(existing_server, dict)
                and existing_server.get(server_name_key) == server_name
            ):
                found_index = i
                break

        if found_index != -1:
            if parent_container[found_index] != server_config:
                logger.info(
                    f"Updating existing MCP server '{server_name}' in {client_key} config list."
                )
                parent_container[found_index] = server_config
                made_changes = True
            else:
                logger.info(
                    f"MCP server '{server_name}' already configured identically in {client_key} config list."
                )
        else:
            logger.info(
                f"Adding new MCP server '{server_name}' to {client_key} config list."
            )
            parent_container.append(server_config)
            made_changes = True

    return made_changes, config_data


# --- Main Installation Function ---


def install_for_client(client_key: str):
    """Handles the configuration update for the specified client."""
    server_name_to_register = "telegram-mcp"

    client_config = MCP_CONFIG_DATA.get(client_key)
    if not client_config:
        logger.error(f"Invalid client key provided: {client_key}")
        raise ValueError(f"Invalid client key: {client_key}")

    client_display_name = client_config["name"]
    is_dict_target = client_config["is_dict_target"]
    server_name_key = client_config.get("server_name_key")
    logger.info(f"Attempting configuration for {client_display_name}")

    try:
        os_type = get_os_type()
        config_path_str = client_config["paths"].get(os_type)
        if not config_path_str:
            logger.error(
                f"No configuration path defined for {client_display_name} on {os_type.upper()}"
            )
            raise FileNotFoundError(
                f"No config path for {client_display_name} on {os_type}"
            )

        config_file_path = resolve_path(config_path_str)
        logger.info(f"Target configuration file: {config_file_path}")

        config_data = load_json_config(config_file_path)

        json_path_keys = client_config["json_path"]
        server_template = client_config["template"]
        new_server_entry = server_template.copy()

        made_changes, updated_config_data = navigate_and_set(
            config_data,
            json_path_keys,
            server_name_to_register,
            new_server_entry,
            client_key,
            is_dict_target,
            server_name_key,
        )

        if made_changes:
            save_json_config(config_file_path, updated_config_data)
            print(
                f"[SUCCESS] {client_display_name} configuration updated successfully."
            )
            print(f"Config file: {config_file_path}")
        else:
            pass

        return True

    except Exception as e:
        print(
            f"[ERROR] Failed to update {client_display_name} configuration. Check logs for details: {e}",
            file=sys.stderr,
        )
        return False
