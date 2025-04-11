"""Grep tool for searching file contents.

Provides pattern-based search functionality across files with filtering capabilities.
"""

import fnmatch
import os
import re
from typing import Any

from code_ally.tools.base import BaseTool
from code_ally.tools.registry import register_tool


@register_tool
class GrepTool(BaseTool):
    """Tool for searching file contents with pattern matching and filtering capabilities."""

    name = "grep"
    description = """Search for a pattern in files with sophisticated filtering.

    <tool_call>
    {"name": "grep", "arguments": {"pattern": "search_term", "path": "/search/directory", "include": "*.py", "case_sensitive": false}}
    </tool_call>
    
    Supports:
    - Regular expression pattern searching
    - File inclusion/exclusion patterns
    - Specific file type filtering
    - Directory depth control
    - Case sensitivity options
    - Whole word matching
    - Optional search and replace functionality
    """
    requires_confirmation = False

    def execute(
        self,
        **kwargs: dict[str, object],
    ) -> dict[str, Any]:
        """Execute the grep tool with the provided kwargs.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            A dictionary with grep search results
        """
        pattern = str(kwargs.get("pattern", ""))
        path = str(kwargs.get("path", "."))
        include = str(kwargs.get("include", "*"))
        exclude = str(kwargs.get("exclude", ""))
        file_types = str(kwargs.get("file_types", ""))

        max_depth_val = kwargs.get("max_depth", -1)
        max_depth = (
            int(max_depth_val) if isinstance(max_depth_val, int | str | float) else -1
        )

        case_sensitive = bool(kwargs.get("case_sensitive", False))
        whole_words = bool(kwargs.get("whole_words", False))
        replace = str(kwargs.get("replace", ""))
        preview_replace = bool(kwargs.get("preview_replace", False))

        max_results_val = kwargs.get("max_results", 100)
        max_results = (
            int(max_results_val)
            if isinstance(max_results_val, int | str | float)
            else 100
        )
        """
        Search for a pattern in files with enhanced filtering options.

        Args:
            pattern: The regex pattern to search for
            path: The directory to search in (defaults to current directory)
            include: File pattern to include in the search (e.g. "*.py")
            exclude: File pattern to exclude from the search (e.g. "*_test.py")
            file_types: Comma-separated list of file extensions (e.g. ".py,.js,.html")
            max_depth: Maximum directory depth to search (-1 for unlimited)
            case_sensitive: Whether the search is case sensitive
            whole_words: Whether to match whole words only
            replace: Replacement text (if provided, performs search and replace)
            preview_replace: Preview replacements without modifying files
            max_results: Maximum number of results to return
            **kwargs: Additional arguments (unused)

        Returns:
            Dict with keys:
                success: Whether the search was successful
                matches: List of matches (file path, line number, line content)
                total_matches: Total number of matches found
                files_searched: Number of files searched
                replacements: List of replacements (if replace was provided)
                error: Error message if any
        """
        try:
            # Expand user home directory if present
            search_dir = os.path.expanduser(path)

            # Verify path doesn't contain traversal patterns
            if (
                ".." in search_dir
                or search_dir.startswith("/")
                or search_dir.startswith("~")
            ):
                # Convert to absolute path to verify CWD constraint
                abs_path = os.path.abspath(search_dir)
                cwd = os.path.abspath(os.getcwd())

                # If it's not within the current working directory, reject it
                if not abs_path.startswith(cwd):
                    return {
                        "success": False,
                        "matches": [],
                        "replacements": [],
                        "total_matches": 0,
                        "files_searched": 0,
                        "error": f"Access denied: Path '{path}' is outside the current working directory. Operations are restricted to '{cwd}' and its subdirectories.",
                    }

            if not os.path.exists(search_dir):
                return {
                    "success": False,
                    "matches": [],
                    "replacements": [],
                    "total_matches": 0,
                    "files_searched": 0,
                    "error": f"Directory not found: {search_dir}",
                }

            if not os.path.isdir(search_dir):
                return {
                    "success": False,
                    "matches": [],
                    "replacements": [],
                    "total_matches": 0,
                    "files_searched": 0,
                    "error": f"Path is not a directory: {search_dir}",
                }

            # Parse file types
            file_extensions = []
            if file_types:
                file_extensions = [
                    ext.strip() if ext.strip().startswith(".") else f".{ext.strip()}"
                    for ext in file_types.split(",")
                ]

            # Prepare regex flags
            flags = 0 if case_sensitive else re.IGNORECASE

            # Handle whole word matching
            if whole_words:
                pattern = r"\b" + pattern + r"\b"

            # Compile the regex pattern
            try:
                regex = re.compile(pattern, flags)
            except re.error as e:
                return {
                    "success": False,
                    "matches": [],
                    "replacements": [],
                    "total_matches": 0,
                    "files_searched": 0,
                    "error": f"Invalid regex pattern: {e}",
                }

            matches = []
            replacements = []
            files_searched = 0
            matched_files = set()

            # Walk through the directory tree with depth control
            for root, dirs, files in os.walk(search_dir):
                # Check depth
                if max_depth >= 0:
                    current_depth = root[len(search_dir) :].count(os.sep)
                    if current_depth > max_depth:
                        dirs[:] = []  # Clear dirs to prevent deeper traversal
                        continue

                for file in files:
                    # Check if the file matches the include pattern
                    if not self._matches_pattern(file, include):
                        continue

                    # Check if the file should be excluded
                    if exclude and self._matches_pattern(file, exclude):
                        continue

                    # Check file extension
                    if file_extensions and not any(
                        file.endswith(ext) for ext in file_extensions
                    ):
                        continue

                    file_path = os.path.join(root, file)

                    # Make sure the file is within the working directory boundary
                    cwd = os.path.abspath(os.getcwd())
                    abs_file_path = os.path.abspath(file_path)
                    if not abs_file_path.startswith(cwd):
                        continue

                    # Skip binary files
                    if self._is_binary_file(file_path):
                        continue

                    files_searched += 1

                    try:
                        # For search and replace, we need to read the entire file
                        with open(file_path, encoding="utf-8") as f:
                            content = f.read()

                        # Check if pattern exists in content (for efficiency)
                        if not regex.search(content):
                            continue

                        # Find matches line by line for reporting
                        lines = content.splitlines()
                        file_matches = []

                        for i, line in enumerate(lines, 1):
                            if regex.search(line):
                                file_matches.append(
                                    {
                                        "file": file_path,
                                        "line": i,
                                        "content": line.strip(),
                                    },
                                )

                        # Add matches to results
                        matches.extend(file_matches)
                        matched_files.add(file_path)

                        # Handle search and replace
                        if (replace or preview_replace) and file_matches:
                            new_content = regex.sub(replace, content)
                            # Only add to replacements if content actually changed
                            if new_content != content:
                                replacements.append(
                                    {
                                        "file": file_path,
                                        "matches": len(file_matches),
                                        "preview": self._get_replacement_preview(
                                            content,
                                            new_content,
                                        ),
                                    },
                                )

                                # If this is not just a preview, write changes back to file
                                if replace and not preview_replace:
                                    with open(
                                        file_path,
                                        "w",
                                        encoding="utf-8",
                                    ) as f:
                                        f.write(new_content)
                    except Exception:
                        # Skip files that can't be read
                        continue

                    # Check if we've reached the max results limit
                    if len(matches) >= max_results:
                        break

                # Exit early if we've reached the max results
                if len(matches) >= max_results:
                    break

            # Sort matches by file modification time (newest first)
            sorted_matches = sorted(
                matches,
                key=lambda m: os.path.getmtime(str(m["file"])),
                reverse=True,
            )

            return {
                "success": True,
                "matches": sorted_matches[:max_results],
                "replacements": replacements,
                "total_matches": len(matches),
                "limited_results": len(matches) > max_results,
                "files_searched": files_searched,
                "error": "",
            }
        except Exception as e:
            return {
                "success": False,
                "matches": [],
                "replacements": [],
                "total_matches": 0,
                "files_searched": 0,
                "error": str(e),
            }

    def _matches_pattern(self, filename: str, pattern: str) -> bool:
        """Check if a filename matches a glob pattern."""
        return fnmatch.fnmatch(filename, pattern)

    def _is_binary_file(self, file_path: str) -> bool:
        """Check if a file is binary."""
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
                return b"\0" in chunk  # Simple heuristic: contains null bytes
        except Exception:
            return True

    def _get_replacement_preview(
        self,
        original: str,
        modified: str,
        context_lines: int = 2,
    ) -> list[dict[str, Any]]:
        """Generate a preview of replacements with surrounding context."""
        original_lines = original.splitlines()
        modified_lines = modified.splitlines()

        preview = []

        # If the files have different numbers of lines, just show a summary
        if len(original_lines) != len(modified_lines):
            return [
                {
                    "summary": f"Changed from {len(original_lines)} to {len(modified_lines)} lines",
                },
            ]

        for i, (orig, mod) in enumerate(
            zip(original_lines, modified_lines, strict=False),
        ):
            if orig != mod:
                # Collect context lines
                start = max(0, i - context_lines)
                end = min(len(original_lines) - 1, i + context_lines)

                context = {
                    "line": i + 1,
                    "before": orig,
                    "after": mod,
                    "context_before": original_lines[start:i] if i > start else [],
                    "context_after": original_lines[i + 1 : end + 1] if i < end else [],
                }
                preview.append(context)

        return preview
