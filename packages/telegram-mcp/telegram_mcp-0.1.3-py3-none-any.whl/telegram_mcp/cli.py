import argparse
import asyncio
import logging
import sys
import os


from . import config  # Keep for run_initial_login HOME_DATA_DIR access
from .client import TelegramClientWrapper
from .server import mcp  # Import the FastMCP instance
from .install import (
    install_for_client,
    MCP_CONFIG_DATA,
)  # Import install function and config data for choices

logger = logging.getLogger(__name__)


# --- Login Function ---
async def run_initial_login() -> bool:
    """Performs the initial blocking login to create the session file. Returns True on success, False on failure."""
    print("-" * 60)
    print(" Telegram MCP Server Initial Login ".center(60, "-"))
    print("-" * 60)
    print("\nAttempting Telegram login...")
    login_wrapper = TelegramClientWrapper()
    login_successful = False
    try:
        login_successful = await login_wrapper.connect(perform_login_if_needed=True)
    except Exception as e:
        # Keep login errors visible even if default level is higher
        logger.error(
            f"An unexpected error occurred during initial login: {e}", exc_info=True
        )
        login_successful = False

    print("-" * 60)
    if login_successful:
        print("[SUCCESS] Initial login complete!")
        print(f"Telegram session saved to {login_wrapper.session_path}")
    else:
        print("[FAILURE] Initial login failed.")
        print("Please check the logs above for errors.")
        print(
            f"Ensure the data directory exists and is writable: {config.HOME_DATA_DIR}"
        )  # Use config path
    print("-" * 60)
    return login_successful


# --- Main Execution Block ---
def main():
    """Main function to handle argument parsing and server execution."""
    # Set default logging level higher for normal operation, but allow override via env var?
    # For now, set directly to ERROR. Login/Install will still print status.
    log_level_str = os.environ.get("TELEGRAM_MCP_LOG_LEVEL", "ERROR").upper()
    log_level = getattr(logging, log_level_str, logging.ERROR)

    logging.basicConfig(
        level=log_level,  # Use ERROR level by default
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    parser = argparse.ArgumentParser(
        description="Telegram MCP Server: Run, Login, or Install for MCP Clients."
    )
    parser.add_argument(
        "--login",
        action="store_true",
        help="Perform the interactive phone login to create/validate the session file.",
    )
    parser.add_argument(
        "--install",
        type=str,
        metavar="CLIENT_KEY",
        choices=MCP_CONFIG_DATA.keys(),  # Use keys from imported config dict
        help=f"Install and configure for a specific client. Handles login if needed. Choices: {', '.join(MCP_CONFIG_DATA.keys())}",
    )

    args = parser.parse_args()

    if args.install:
        client_key = args.install
        # Use INFO level specifically for install process feedback
        logging.getLogger().setLevel(logging.INFO)
        logger.info(
            f"\n--- Starting Installation for {MCP_CONFIG_DATA[client_key]['name']} ---"
        )

        # 1. Ensure Login first (essential before configuring)
        temp_wrapper = TelegramClientWrapper()
        if not temp_wrapper.session_path.exists():
            logger.info("Telegram session file not found. Initiating login...")
            # run_initial_login prints its own status
            login_ok = asyncio.run(run_initial_login())
            if not login_ok:
                logger.error("[ERROR] Login failed. Cannot proceed with installation.")
                sys.exit(1)
            logger.info("Login successful.")
        else:
            logger.info(
                f"Existing session found at {temp_wrapper.session_path}. Skipping login."
            )

        # 2. Call the installation function from the install module
        logger.info(
            f"Updating {MCP_CONFIG_DATA[client_key]['name']} MCP configuration..."
        )
        install_successful = install_for_client(client_key)

        if install_successful:
            # Success messages are printed within install_for_client
            print(
                "\nYou can now run the server using: telegram-mcp"
            )  # Keep final user instruction
            sys.exit(0)
        else:
            # Error messages are printed within install_for_client
            sys.exit(1)

    elif args.login:
        # Use INFO level specifically for login process feedback
        logging.getLogger().setLevel(logging.INFO)
        logger.info("Running initial login process only...")
        # run_initial_login prints its own status
        login_ok = asyncio.run(run_initial_login())
        sys.exit(0 if login_ok else 1)

    else:
        # Default: Start the MCP server (uses default ERROR level set above)
        logger.info(
            "Starting Telegram MCP server..."
        )  # This INFO won't show by default now
        try:
            mcp.run()  # Starts the server and blocks
            logger.info("Telegram MCP server stopped normally.")  # Won't show
        except KeyboardInterrupt:
            logger.info("Server stopped by user (KeyboardInterrupt).")  # Won't show
        except Exception as e:
            # Critical errors should always be logged
            logger.critical(f"Fatal error running MCP server: {e}", exc_info=True)
            sys.exit(1)
        finally:
            logger.info("Server process exiting.")  # Won't show
        sys.exit(0)


# This allows running the CLI directly using `python -m telegram_mcp.cli`
if __name__ == "__main__":
    main()
