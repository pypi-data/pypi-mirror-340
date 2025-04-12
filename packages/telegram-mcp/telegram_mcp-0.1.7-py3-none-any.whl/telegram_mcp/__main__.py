import sys
import runpy

# This allows running the package directly using `python -m telegram_mcp`
# It effectively executes the main function defined in cli.py

if __name__ == "__main__":
    # We need to ensure that when runpy executes cli, cli.__name__ is "__main__"
    # so that its own `if __name__ == "__main__":` block runs.
    # runpy handles sys.argv adjustments automatically when alter_sys=True.
    try:
        runpy.run_module("telegram_mcp.cli", run_name="__main__", alter_sys=True)
    except ImportError as e:
        # Provide helpful error if cli cannot be imported (e.g., structure issue)
        print(f"Error: Could not run telegram_mcp.cli. {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)
