"""
Safe file listing function for the AI agent.

Lists files and directories with security guardrails to prevent
directory traversal attacks.
"""

import os
from typing import List
from google.genai import types


def _is_within_directory(base: str, target: str) -> bool:
    """Check if target path is within base directory.
    
    Args:
        base: The base directory path.
        target: The target path to check.
        
    Returns:
        True if target is within base, False otherwise.
    """
    base_abs = os.path.abspath(base)
    target_abs = os.path.abspath(target)
    try:
        common = os.path.commonpath([base_abs, target_abs])
    except ValueError:
        return False
    return common == base_abs


def _format_entry_line(name: str, path: str) -> str:
    """Format a file/directory entry for display.
    
    Args:
        name: The name of the entry.
        path: The absolute path to the entry.
        
    Returns:
        A formatted string with file info.
    """
    try:
        is_dir = os.path.isdir(path)
        size = os.path.getsize(path)
        return f"- {name}: file_size={size} bytes, is_dir={str(is_dir)}"
    except Exception as exc:
        return f"- {name}: Error: {exc}"


def get_files_info(working_directory: str, directory: str = ".") -> str:
    """List files in the specified directory.
    
    Args:
        working_directory: The base working directory.
        directory: The directory to list, relative to working_directory.
        
    Returns:
        A formatted string with directory contents or error message.
    """
    try:
        full_path = os.path.join(working_directory, directory)

        if not _is_within_directory(working_directory, full_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'

        entries: List[str] = []
        for name in os.listdir(full_path):
            entry_path = os.path.join(full_path, name)
            entries.append(_format_entry_line(name, entry_path))

        return "\n".join(entries)
    except Exception as exc:
        return f"Error: {exc}"


# Expose the function declaration schema for the LLM tools API
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description=(
        "Lists files in the specified directory along with their sizes, constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself."
                ),
            )
        },
    ),
)


