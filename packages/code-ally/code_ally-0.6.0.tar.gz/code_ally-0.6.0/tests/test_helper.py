"""Test helper functions and fixtures for CodeAlly tests."""

import os
import sys
from typing import Any
from unittest.mock import MagicMock

# Add the root directory to the path for direct imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def setup_mocks() -> None:
    """Set up common mocks to avoid import errors."""

    # Create a StdoutProxy class for pytest to use instead of the prompt_toolkit one
    # This fixes issues with Python 3.13's stricter isinstance() checks
    class StdoutProxy:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self.original_stdout = sys.stdout

    # Mock prompt_toolkit
    mock_pt = MagicMock()
    mock_pt.key_binding = MagicMock()
    mock_pt.shortcuts = MagicMock()
    mock_pt.styles = MagicMock()
    mock_pt.history = MagicMock()
    mock_pt.completion = MagicMock()

    # Set up patch_stdout module with our StdoutProxy class
    mock_patch_stdout = MagicMock()
    mock_patch_stdout.StdoutProxy = StdoutProxy
    mock_pt.patch_stdout = mock_patch_stdout

    # Add PromptSession class that returns a simple mock
    class MockPromptSession:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass

        def prompt(self, *args: Any, **kwargs: Any) -> str:
            return "Mock user input"

    mock_pt.PromptSession = MockPromptSession

    # Mock prompt_toolkit modules
    sys.modules["prompt_toolkit"] = mock_pt
    sys.modules["prompt_toolkit.key_binding"] = mock_pt.key_binding
    sys.modules["prompt_toolkit.shortcuts"] = mock_pt.shortcuts
    sys.modules["prompt_toolkit.styles"] = mock_pt.styles
    sys.modules["prompt_toolkit.history"] = mock_pt.history
    sys.modules["prompt_toolkit.completion"] = mock_pt.completion
    sys.modules["prompt_toolkit.patch_stdout"] = mock_pt.patch_stdout

    # Also mock the output module which is causing the issue
    mock_output = MagicMock()
    mock_defaults = MagicMock()

    # Replace the problematic create_output function
    def mock_create_output(*args: Any, **kwargs: Any) -> MagicMock:
        return MagicMock()

    mock_defaults.create_output = mock_create_output
    mock_output.defaults = mock_defaults
    sys.modules["prompt_toolkit.output"] = mock_output
    sys.modules["prompt_toolkit.output.defaults"] = mock_defaults

    # Create a comprehensive set of mocks for rich
    mock_rich = MagicMock()
    rich_modules = [
        "console",
        "live",
        "markdown",
        "syntax",
        "panel",
        "table",
        "box",
        "progress",
        "prompt",
        "theme",
        "spinner",
        "text",
        "style",
        "color",
        "columns",
        "align",
        "rule",
        "status",
        "logging",
        "pretty",
        "measure",
    ]

    # Set attributes in mock_rich and create module mocks
    for module in rich_modules:
        setattr(mock_rich, module, MagicMock())
        sys.modules[f"rich.{module}"] = getattr(mock_rich, module)

    # Set the main rich module
    sys.modules["rich"] = mock_rich
