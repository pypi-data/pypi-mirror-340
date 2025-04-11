"""
Agent subpackage for Code Ally - Local LLM-powered pair programming assistant.

Contains classes and modules that handle conversation flow, UI, and tools.
"""

__all__ = ["Agent", "PermissionManager", "ToolManager"]

from .agent import Agent
from .permission_manager import PermissionManager
from .tool_manager import ToolManager
