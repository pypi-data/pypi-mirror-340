"""File reading tool module for Code Ally.

This module provides enhanced file reading capabilities including support for
line ranges, pattern matching, section extraction, and delimited content.
"""

import os
import re
from typing import Any

from code_ally.tools.base import BaseTool
from code_ally.tools.registry import register_tool


@register_tool
class FileReadTool(BaseTool):
    """Tool for reading file contents with advanced filtering options.

    Supports line ranges, pattern matching, and section extraction features.
    """

    name = "file_read"
    description = """Read the contents of a file with context-efficient options.

    <tool_call>
    {"name": "file_read", "arguments": {"path": "/path/to/file.txt", "start_line": 0, "max_lines": 100}}
    </tool_call>
    
    Supports:
    - Reading specific line ranges (start_line, max_lines)
    - Searching for patterns with context (search_pattern, context_lines)
    - Reading sections based on delimiters (from_delimiter, to_delimiter)
    - Finding sections by headings or markers (section_pattern)
    """
    requires_confirmation = False

    def execute(
        self,
        **kwargs: dict[str, object],
    ) -> dict[str, Any]:
        """Execute the read tool with the provided kwargs.

        Args:
            **kwargs: Tool-specific parameters

        Returns:
            A dictionary with file read results
        """
        path = str(kwargs.get("path", ""))
        start_line_val = kwargs.get("start_line", 0)
        start_line = (
            int(start_line_val) if isinstance(start_line_val, int | str | float) else 0
        )

        max_lines_val = kwargs.get("max_lines", 0)
        max_lines = (
            int(max_lines_val) if isinstance(max_lines_val, int | str | float) else 0
        )

        search_pattern = str(kwargs.get("search_pattern", ""))

        context_lines_val = kwargs.get("context_lines", 3)
        context_lines = (
            int(context_lines_val)
            if isinstance(context_lines_val, int | str | float)
            else 3
        )

        from_delimiter = str(kwargs.get("from_delimiter", ""))
        to_delimiter = str(kwargs.get("to_delimiter", ""))
        section_pattern = str(kwargs.get("section_pattern", ""))
        r"""
        Read the contents of a file with options to target specific sections or search results.

        Tracks file content hashes to ensure only one copy of a file is kept in conversation
        context at a time. If a file is read multiple times, earlier instances are removed.

        Args:
            path: The path to the file to read
            start_line: Line number to start reading from (0-based, default: 0)
            max_lines: Maximum number of lines to read (0 for all, default: 0)
            search_pattern: Optional pattern to search within the file
            context_lines: Number of lines before/after matches to include (default: 3)
            from_delimiter: Start reading from this delimiter pattern (e.g., "# Section 1")
            to_delimiter: Stop reading at this delimiter pattern
            section_pattern: Extract sections matching this pattern (e.g., "## [\\w\\s]+")
            **kwargs: Additional arguments (unused)

        Returns:
            Dict with keys:
                success: Whether the file was read successfully
                content: The file's contents or matching sections
                line_count: Total number of lines in the file
                read_lines: Number of lines that were read
                file_size: Size of the file in bytes
                is_partial: Whether the content is a partial view
                is_binary: Whether the file appears to be binary
                error: Error message if any
                previous_message_id: ID of a previous message containing this file (if duplicate)
        """
        try:
            # Expand user home directory if present
            file_path = os.path.expanduser(path)

            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "content": "",
                    "line_count": 0,
                    "read_lines": 0,
                    "file_size": 0,
                    "is_partial": False,
                    "is_binary": False,
                    "error": f"File not found: {file_path}",
                }

            if not os.path.isfile(file_path):
                return {
                    "success": False,
                    "content": "",
                    "line_count": 0,
                    "read_lines": 0,
                    "file_size": 0,
                    "is_partial": False,
                    "is_binary": False,
                    "error": f"Path is not a file: {file_path}",
                }

            # Get file size
            file_size = os.path.getsize(file_path)

            # Check if file might be binary
            is_binary = self._is_binary_file(file_path)
            if is_binary:
                return {
                    "success": True,
                    "content": "[Binary file]",
                    "line_count": 0,
                    "read_lines": 0,
                    "file_size": file_size,
                    "is_partial": True,
                    "is_binary": True,
                    "error": "",
                }

            # If delimiters are provided, use those for reading
            if from_delimiter or to_delimiter:
                content, lines_read, total_lines = self._read_with_delimiters(
                    file_path,
                    from_delimiter,
                    to_delimiter,
                )
                is_partial = lines_read < total_lines

            # If section pattern is provided, extract matching sections
            elif section_pattern:
                content, sections_found, total_lines = self._read_sections(
                    file_path,
                    section_pattern,
                )
                lines_read = sections_found if sections_found > 0 else 0
                is_partial = True  # Section extraction is always partial

            # If search pattern is provided, use search reading
            elif search_pattern:
                content, matches, total_lines = self._read_with_pattern(
                    file_path,
                    search_pattern,
                    context_lines,
                    start_line,
                    max_lines,
                )
                read_lines = len(matches) if matches else 0
                is_partial = read_lines < total_lines

            # Otherwise use standard line-based reading
            else:
                content, lines_read, total_lines = self._read_with_limits(
                    file_path,
                    start_line,
                    max_lines,
                )
                is_partial = lines_read < total_lines

            result = {
                "success": True,
                "content": content,
                "line_count": total_lines,
                "read_lines": lines_read if "lines_read" in locals() else 0,
                "file_size": file_size,
                "is_partial": is_partial,
                "is_binary": False,
                "error": "",
                "file_path": file_path,  # Include the file path for tracking
            }

            # Check for duplicate file content by getting service registry
            from code_ally.service_registry import ServiceRegistry

            service_registry = ServiceRegistry.get_instance()

            # If token manager is available, check for duplicates
            if service_registry and service_registry.has_service("token_manager"):
                token_manager = service_registry.get("token_manager")
                # Note: message_id will be assigned by the agent when processing the tool response
                result["_needs_duplicate_check"] = True

            return result
        except Exception as exc:
            return {
                "success": False,
                "content": "",
                "line_count": 0,
                "read_lines": 0,
                "file_size": 0,
                "is_partial": False,
                "is_binary": False,
                "error": str(exc),
            }

    def _is_binary_file(self, file_path: str) -> bool:
        """Check if a file appears to be binary.

        Args:
            file_path: Path to the file

        Returns:
            True if the file appears to be binary, False otherwise
        """
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
                return b"\0" in chunk  # Simple heuristic: contains null bytes
        except Exception:
            return False

    def _count_lines(self, file_path: str) -> int:
        """Count lines in a file efficiently.

        Args:
            file_path: Path to the file

        Returns:
            Number of lines in the file
        """
        lines = 0
        with open(file_path, encoding="utf-8", errors="replace") as f:
            # Use buffer read and count newlines for efficiency
            buf_size = 1024 * 1024
            read_f = f.read
            buf = read_f(buf_size)
            while buf:
                lines += buf.count("\n")
                buf = read_f(buf_size)
        return lines

    def _read_with_limits(
        self,
        file_path: str,
        start_line: int,
        max_lines: int,
    ) -> tuple[str, int, int]:
        """Read a file with line limits.

        Args:
            file_path: Path to the file
            start_line: Line to start reading from (0-based)
            max_lines: Maximum number of lines to read

        Returns:
            Tuple of (content, lines_read, total_lines)
        """
        content = []
        current_line = 0
        lines_read = 0

        with open(file_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                if current_line >= start_line:
                    if max_lines > 0 and lines_read >= max_lines:
                        break
                    content.append(line.rstrip())
                    lines_read += 1
                current_line += 1

        # Add indicators for partial content
        result = "\n".join(content)
        if start_line > 0:
            result = f"[...] (skipped {start_line} lines)\n" + result

        if max_lines > 0 and current_line > start_line + lines_read:
            result += "\n[...] (more lines not shown)"

        return result, lines_read, current_line

    def _read_with_delimiters(
        self,
        file_path: str,
        from_delimiter: str,
        to_delimiter: str,
    ) -> tuple[str, int, int]:
        """Read a file between specified delimiters.

        Args:
            file_path: Path to the file
            from_delimiter: Start reading from this pattern
            to_delimiter: Stop reading at this pattern

        Returns:
            Tuple of (content, lines_read, total_lines)
        """
        content = []
        total_lines = 0
        lines_read = 0
        in_section = (
            from_delimiter == ""
        )  # If no start delimiter, start capturing immediately

        with open(file_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                total_lines += 1

                # Check for start delimiter if we're not already in a section
                if not in_section and from_delimiter and from_delimiter in line:
                    in_section = True
                    content.append(line.rstrip())
                    lines_read += 1
                    continue

                # If we're in a section, capture the line
                if in_section:
                    # Check if we've reached the end delimiter
                    if to_delimiter and to_delimiter in line:
                        content.append(line.rstrip())
                        lines_read += 1
                        break

                    content.append(line.rstrip())
                    lines_read += 1

        # If we didn't find any section
        if not content:
            return (
                f"No content found between '{from_delimiter}' and '{to_delimiter}'",
                0,
                total_lines,
            )

        result = "\n".join(content)

        # Add indicators for partial content
        if lines_read < total_lines:
            result += "\n[...] (more lines not shown)"

        return result, lines_read, total_lines

    def _read_sections(
        self,
        file_path: str,
        section_pattern: str,
    ) -> tuple[str, int, int]:
        """Extract sections matching a pattern from a file.

        Args:
            file_path: Path to the file
            section_pattern: Regex pattern that identifies section headers

        Returns:
            Tuple of (content, sections_found, total_lines)
        """
        try:
            section_regex = re.compile(section_pattern)
        except re.error:
            return f"Invalid regex pattern: {section_pattern}", 0, 0

        content: list[str] = []
        total_lines = 0
        sections_found = 0
        current_section: list[str] = []
        in_section = False

        with open(file_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                total_lines += 1

                # Check if this line is a section header
                if section_regex.search(line):
                    # If we were already in a section, save it
                    if in_section and current_section:
                        content.extend(current_section)
                        content.append("")  # Add a blank line between sections

                    # Start a new section
                    current_section = [line.rstrip()]
                    in_section = True
                    sections_found += 1
                elif in_section:
                    current_section.append(line.rstrip())

        # Add the last section if we have one
        if in_section and current_section:
            content.extend(current_section)

        if not content:
            return f"No sections matching '{section_pattern}' found", 0, total_lines

        return "\n".join(content), sections_found, total_lines

    def _read_with_pattern(
        self,
        file_path: str,
        pattern: str,
        context_lines: int,
        start_line: int,
        max_lines: int,
    ) -> tuple[str, list[tuple[int, str]], int]:
        """Read a file and extract sections matching a pattern.

        Args:
            file_path: Path to the file
            pattern: Pattern to search for
            context_lines: Number of context lines around matches
            start_line: Line to start reading from
            max_lines: Maximum matches to include (0 for all)

        Returns:
            Tuple of (content, matching_line_numbers, total_lines)
        """
        import re  # pylint: disable=import-outside-toplevel

        try:
            pattern_re = re.compile(pattern)
        except re.error:
            # Fall back to basic string search if regex is invalid
            pattern_re = None

        matches: list[tuple[int, str]] = []
        context_blocks: list[list[tuple[int, str]]] = []
        total_lines = 0
        match_count = 0

        # First pass: find matching lines
        with open(file_path, encoding="utf-8", errors="replace") as f:
            lines = []
            for i, line in enumerate(f):
                if i < start_line:
                    continue

                lines.append(line.rstrip())
                total_lines = i + 1

                # Check for pattern match
                if (
                    pattern_re
                    and pattern_re.search(line)
                    or pattern_re is None
                    and pattern in line
                ):
                    matches.append((i, line))
                    match_count += 1

                # Stop if we've reached max matches
                if max_lines > 0 and match_count >= max_lines:
                    break

        # No matches found
        if not matches:
            return f"No matches found for pattern: {pattern}", [], total_lines

        # Second pass: build context blocks
        for match_tuple in matches:
            match_line = match_tuple[0]  # Extract line number from tuple
            start = max(0, match_line - context_lines)
            end = min(len(lines) - 1, match_line + context_lines)

            # Add separator between non-contiguous blocks
            if context_blocks and start > context_blocks[-1][1] + 1:
                context_blocks.append((-1, -1))  # Sentinel for separator

            # Add this block or extend previous block
            if not context_blocks or start > context_blocks[-1][1]:
                context_blocks.append((start, end))
            else:
                # Extend previous block
                context_blocks[-1] = (context_blocks[-1][0], end)

        # Build final content with appropriate separators and line numbers
        result = []
        for _, (start, end) in enumerate(context_blocks):
            if start == -1:  # Sentinel for separator
                result.append("\n[...] (skipped lines)\n")
                continue

            block_lines = []
            for j in range(start, end + 1):
                line_num = j + 1  # Convert to 1-based numbering for display
                if any(match[0] == j for match in matches):
                    block_lines.append(f"{line_num}: >> {lines[j]}")
                else:
                    block_lines.append(f"{line_num}:    {lines[j]}")

            result.append("\n".join(block_lines))

        return "\n".join(result), matches, total_lines
