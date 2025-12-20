"""
Safe Python file execution function for the AI agent.

Executes Python files with subprocess isolation and timeout protection.
"""

import os
import subprocess
from typing import List, Optional
from google.genai import types

# Timeout for script execution in seconds
EXECUTION_TIMEOUT_SECONDS = 30


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


def run_python_file(
    working_directory: str, file_path: str, args: Optional[List[str]] = None
) -> str:
    """Execute a Python file with optional arguments.
    
    Args:
        working_directory: The base working directory.
        file_path: The path to the Python file, relative to working_directory.
        args: Optional list of command-line arguments.
        
    Returns:
        The stdout/stderr output or error message.
    """
    try:
        if args is None:
            args = []

        full_path = os.path.join(working_directory, file_path)
        if not _is_within_directory(working_directory, full_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.exists(full_path):
            return f'Error: File "{file_path}" not found.'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        # Execute using file_path relative to the working directory to avoid duplicating the path
        cmd = ["python", file_path, *args]
        try:
            completed = subprocess.run(
                cmd,
                cwd=working_directory,
                capture_output=True,
                text=True,
                timeout=EXECUTION_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired:
            return f"Error: Script execution timed out after {EXECUTION_TIMEOUT_SECONDS} seconds"
        except Exception as exc:
            return f"Error executing Python file: {exc}"

        stdout = completed.stdout.strip()
        stderr = completed.stderr.strip()

        if not stdout and not stderr and completed.returncode == 0:
            return "No output produced."

        parts = []
        if stdout:
            parts.append(f"STDOUT:\n{stdout}")
        if stderr:
            parts.append(f"STDERR:\n{stderr}")
        if completed.returncode != 0:
            parts.append(f"Process exited with code {completed.returncode}")
        return "\n".join(parts)
    except Exception as exc:
        return f"Error: {exc}"


# Function schema for tools API
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file with optional args, returning STDOUT/STDERR and exit code."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Relative path of the Python file to execute.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional list of string args to pass to the program.",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)


