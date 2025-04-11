#!/usr/bin/env python3
"""Code Ally main entry point.

This module contains the main function and command-line interface for the
Code Ally application. It handles argument parsing, configuration management,
and initializing the agent with the appropriate tools and models.
"""

import argparse
import json
import logging
import signal
import sys
import types

import requests  # type: ignore
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel

from code_ally.agent import Agent
from code_ally.config import ConfigManager
from code_ally.llm_client import OllamaClient
from code_ally.prompts import get_main_system_prompt
from code_ally.service_registry import ServiceRegistry
from code_ally.tools import ToolRegistry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
logger = logging.getLogger("code_ally")

# Global reference to the agent for signal handling - needed to differentiate
# Ctrl+C during requests vs. Ctrl+C when idle.
_global_agent: Agent | None = None


def handle_interrupt(signum: int, frame: types.FrameType | None) -> None:
    """Handle keyboard interrupt (SIGINT) signals.

    - If an LLM request is in progress, let the exception propagate to the OllamaClient
      which will handle interrupting the request properly.
    - Otherwise (idle or during user input), exit gracefully.
    """
    global _global_agent

    # Check if an agent exists and if its request_in_progress flag is set
    if _global_agent and getattr(_global_agent, "request_in_progress", False):
        # If a request is in progress, we now want to propagate the signal
        # to the OllamaClient which will handle it properly
        logger.debug(
            "SIGINT caught by main handler during request. Propagating to client...",
        )
        # We don't return here - let the signal propagate to the client
    else:
        # If no request is active, exit gracefully
        logger.debug("SIGINT caught by main handler (no request active). Exiting.")
        console = Console()
        console.print("\n[bold]Goodbye![/]")
        sys.exit(0)


def configure_logging(verbose: bool) -> None:
    """Configure logging level based on verbose flag.

    Args:
        verbose: Whether to enable verbose logging
    """
    if verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    else:
        logger.setLevel(logging.INFO)


def check_ollama_availability(
    endpoint: str,
    model: str,
) -> tuple[bool, bool, str | None]:
    """Check if Ollama is running and the specified model is available.

    Makes an HTTP request to the Ollama API to check if the server is running
    and if the specified model is available for use.

    Args:
        endpoint: The Ollama API endpoint URL (e.g. http://localhost:11434)
        model: The model name to check (e.g. "llama3" or "qwen:7b")

    Returns:
        tuple: (is_running, model_available, error_message)
            - is_running: True if Ollama server is responding
            - model_available: True if the model is available
            - error_message: Description of any error or None if successful
    """
    logger.debug(f"Checking Ollama availability at {endpoint} for model {model}")

    # Check if Ollama server is running
    try:
        response = requests.get(f"{endpoint}/api/tags", timeout=5)
        response.raise_for_status()

        # Server is running, check if the model is available
        data = response.json()

        if "models" not in data:
            logger.warning("Unexpected response format from Ollama API")
            return True, False, "Unexpected response format from Ollama API"

        available_models = [model_data["name"] for model_data in data["models"]]
        logger.debug(f"Available models: {available_models}")

        if model in available_models:
            logger.info(f"Model '{model}' is available")
            return True, True, None
        else:
            logger.warning(f"Model '{model}' is not available in Ollama")
            return True, False, f"Model '{model}' is not available in Ollama"

    except requests.exceptions.ConnectionError:
        logger.error(f"Could not connect to Ollama at {endpoint}")
        return False, False, f"Could not connect to Ollama at {endpoint}"
    except requests.exceptions.Timeout:
        logger.error("Connection to Ollama timed out")
        return False, False, "Connection to Ollama timed out"
    except requests.exceptions.RequestException as e:
        logger.error(f"Error connecting to Ollama: {str(e)}")
        return False, False, f"Error connecting to Ollama: {str(e)}"
    except (KeyError, ValueError) as e:
        logger.error(f"Error parsing Ollama response: {str(e)}")
        return True, False, f"Error parsing Ollama response: {str(e)}"


def print_ollama_instructions(endpoint: str, model: str, error_message: str) -> None:
    """Print instructions for setting up Ollama.

    Args:
        endpoint: The Ollama API endpoint
        model: The model name
        error_message: The specific error message
    """
    console = Console()

    instructions = f"""
1. Make sure Ollama is installed:
   - Download from: https://ollama.ai
   - Follow the installation instructions for your platform

2. Start the Ollama server:
   - Run the Ollama application
   - Or start it from the command line: `ollama serve`

3. Pull the required model:
   - Run: `ollama pull {model}`

4. Verify Ollama is running:
   - Run: `curl {endpoint}/api/tags`
   - You should see a JSON response with available models

Current error: {error_message}
    """

    console.print(
        Panel(
            instructions,
            title="[bold yellow]⚠️ Ollama Configuration Required[/]",
            border_style="yellow",
            expand=False,
        ),
    )


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    config_manager = ConfigManager.get_instance()
    config = config_manager.get_config()

    parser = argparse.ArgumentParser(
        description="Code Ally - Local LLM-powered pair programming assistant",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Model and API settings
    model_group = parser.add_argument_group("Model Settings")
    model_group.add_argument(
        "--model",
        default=config.get("model"),
        help="The model to use",
    )
    model_group.add_argument(
        "--endpoint",
        default=config.get("endpoint"),
        help="The Ollama API endpoint URL",
    )
    model_group.add_argument(
        "--temperature",
        type=float,
        default=config.get("temperature"),
        help="Temperature for text generation (0.0-1.0)",
    )
    model_group.add_argument(
        "--context-size",
        type=int,
        default=config.get("context_size"),
        help="Context size in tokens",
    )
    model_group.add_argument(
        "--max-tokens",
        type=int,
        default=config.get("max_tokens"),
        help="Maximum tokens to generate",
    )

    # Configuration management
    config_group = parser.add_argument_group("Configuration")
    config_group.add_argument(
        "--config",
        action="store_true",
        help="Save the current command line options as config defaults",
    )
    config_group.add_argument(
        "--config-show",
        action="store_true",
        help="Show the current configuration",
    )
    config_group.add_argument(
        "--config-reset",
        action="store_true",
        help="Reset configuration to defaults",
    )

    # Security and behavior settings
    security_group = parser.add_argument_group("Security and Behavior")
    security_group.add_argument(
        "--yes-to-all",
        action="store_true",
        help="Skip all confirmation prompts (dangerous, use with caution)",
    )
    security_group.add_argument(
        "--check-context-msg",
        action="store_true",
        dest="check_context_msg",
        default=config.get("check_context_msg"),
        help="Encourage LLM to check its context when redundant tool calls are detected",
    )
    security_group.add_argument(
        "--no-auto-dump",
        action="store_false",
        dest="auto_dump",
        default=config.get("auto_dump", True),
        help="Disable automatic conversation dump when exiting",
    )

    # Debug and diagnostics
    debug_group = parser.add_argument_group("Debug and Diagnostics")
    debug_group.add_argument(
        "--skip-ollama-check",
        action="store_true",
        help="Skip the check for Ollama availability",
    )
    debug_group.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose mode with detailed logging",
    )
    debug_group.add_argument(
        "--debug-tool-calls",
        action="store_true",
        help="Print raw tool calls for debugging",
    )

    return parser.parse_args()


def handle_config_commands(args: argparse.Namespace) -> bool:
    """Handle configuration-related commands."""
    console = Console()

    # Show current configuration
    if args.config_show:
        console.print(json.dumps(ConfigManager.get_instance().get_config(), indent=2))
        return True

    # Reset configuration to defaults
    if args.config_reset:
        ConfigManager.get_instance().reset()
        console.print("[green]Configuration reset to defaults[/]")
        return True

    # Save current settings as new defaults
    if args.config:
        config_manager = ConfigManager.get_instance()
        new_config = config_manager.get_config().copy()
        new_config.update(
            {
                "model": args.model,
                "endpoint": args.endpoint,
                "temperature": args.temperature,
                "context_size": args.context_size,
                "max_tokens": args.max_tokens,
                "auto_confirm": args.yes_to_all,
                "check_context_msg": args.check_context_msg,
                "auto_dump": args.auto_dump,
            },
        )
        for key, value in new_config.items():
            config_manager.set_value(key, value)
        console.print("[green]Configuration saved successfully[/]")
        return True

    return False


def main() -> None:
    """Main entry point for the application."""
    # Create console for rich output
    console = Console()

    # Parse command line arguments
    args = parse_args()

    # Configure logging based on verbose flag
    configure_logging(args.verbose)

    # Handle configuration commands (these don't require Ollama)
    if handle_config_commands(args):
        return

    # Check if Ollama is configured correctly (unless explicitly skipped)
    if not args.skip_ollama_check:
        console.print("[bold]Checking Ollama availability...[/]")
        is_running, model_available, error_message = check_ollama_availability(
            args.endpoint,
            args.model,
        )

        if not is_running or not model_available:
            console.print(f"[bold red]Error:[/] {error_message or 'Unknown error'}")
            print_ollama_instructions(
                args.endpoint,
                args.model,
                error_message or "Unknown error",
            )

            # Ask user if they want to continue anyway
            continue_anyway = input("Do you want to continue anyway? (y/n): ").lower()
            if continue_anyway not in ("y", "yes"):
                console.print(
                    "[yellow]Exiting. Please configure Ollama and try again.[/]",
                )
                return

            console.print("[yellow]Continuing without validated Ollama setup...[/]")
        else:
            console.print(
                f"[green]✓ Ollama is running and model '{args.model}' is available[/]",
            )

    # Determine client type based on model name
    client_type = "default"  # Assign a default string value
    if "qwen" in args.model.lower():
        # For Qwen models, detect if we're using Ollama
        if args.endpoint and "ollama" in args.endpoint.lower():
            client_type = "ollama"
        else:
            # Default for Qwen models is to use Qwen-Agent style formatting
            client_type = "qwen_agent"

    # Create the LLM client with appropriate type
    model_client = OllamaClient(
        endpoint=args.endpoint,
        model_name=args.model,
        temperature=args.temperature,
        context_size=args.context_size,
        max_tokens=args.max_tokens,
        keep_alive=60,  # seconds
    )

    # Get tools from the registry
    tools = ToolRegistry().get_tool_instances()

    # Get the system prompt
    system_prompt = get_main_system_prompt()

    # Create and register services
    service_registry = ServiceRegistry.get_instance()
    config_manager = ConfigManager.get_instance()
    service_registry.register("config_manager", config_manager)

    # Create the agent with service registry
    agent = Agent(
        model_client=model_client,
        client_type=client_type,
        tools=tools,
        system_prompt=system_prompt,
        verbose=args.verbose,
        check_context_msg=args.check_context_msg,
        auto_dump=args.auto_dump,
        service_registry=service_registry,
    )

    # Set debug options
    if args.debug_tool_calls:
        logging.getLogger("code_ally.agent").setLevel(logging.DEBUG)

    # Set auto-confirm if specified
    if args.yes_to_all:
        agent.trust_manager.set_auto_confirm(True)
        logger.warning("Auto-confirm mode enabled - will skip all confirmation prompts")

    # Set up the global agent reference for the signal handler
    global _global_agent  # Use global scope for the signal handler's access
    _global_agent = agent

    # Install signal handler for SIGINT (Ctrl+C)
    signal.signal(signal.SIGINT, handle_interrupt)

    try:
        agent.run_conversation()
    except KeyboardInterrupt:
        # This catches KeyboardInterrupt raised when the user cancels the input prompt
        # or if the signal handler decided to exit (i.e., no request was active).
        logger.debug(
            "KeyboardInterrupt caught in main execution block (likely prompt cancellation or idle interrupt).",
        )
        if agent.auto_dump:
            try:
                agent.command_handler.dump_conversation(agent.messages, "")
                console.print("\n[bold]Goodbye![/]")
            except Exception as e:
                console.print(f"\n[bold red]Error during auto-dump: {str(e)}[/]")
                console.print("[bold]Goodbye![/]")
        else:
            console.print("\n[bold]Goodbye![/]")
        sys.exit(0)
    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Error connecting to Ollama:[/] {str(e)}")
        print_ollama_instructions(args.endpoint, args.model, str(e))
        sys.exit(1)
    except Exception as e:
        logger.exception("Unexpected error occurred:")
        console.print(f"\n[bold red]Unexpected error:[/] {str(e)}")
        if args.verbose:
            import traceback

            console.print(
                Panel(
                    traceback.format_exc(),
                    title="[bold red]Error Details[/]",
                    border_style="red",
                ),
            )
        sys.exit(1)


if __name__ == "__main__":
    main()
