import os
from typing import List
from google.genai import types


def _is_within_directory(base: str, target: str) -> bool:
    base_abs = os.path.abspath(base)
    target_abs = os.path.abspath(target)
    try:
        common = os.path.commonpath([base_abs, target_abs])
    except ValueError:
        return False
    return common == base_abs


def _format_entry_line(name: str, path: str) -> str:
    try:
        is_dir = os.path.isdir(path)
        size = os.path.getsize(path)
        return f"- {name}: file_size={size} bytes, is_dir={str(is_dir)}"
    except Exception as exc:
        return f"- {name}: Error: {exc}"


def get_files_info(working_directory: str, directory: str = ".") -> str:
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


