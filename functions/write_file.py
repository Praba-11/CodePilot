"""
Safe file writing function for the AI agent.

Creates or overwrites files with security guardrails to prevent
directory traversal attacks.
"""

import os
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


def write_file(working_directory: str, file_path: str, content: str) -> str:
    """Write or create a file with the given content.
    
    Args:
        working_directory: The base working directory.
        file_path: The path to the file, relative to working_directory.
        content: The content to write.
        
    Returns:
        Success message or error message.
    """
    try:
        full_path = os.path.join(working_directory, file_path)
        if not _is_within_directory(working_directory, full_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        parent_dir = os.path.dirname(full_path)
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as exc:
        return f"Error: {exc}"


# Function schema for tools API
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Creates or overwrites a file with the given content, constrained to the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path of the file to write.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the file.",
            ),
        },
    ),
)


