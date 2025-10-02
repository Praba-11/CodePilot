import os
from .config import MAX_FILE_CHARS
from google.genai import types


def _is_within_directory(base: str, target: str) -> bool:
    base_abs = os.path.abspath(base)
    target_abs = os.path.abspath(target)
    try:
        common = os.path.commonpath([base_abs, target_abs])
    except ValueError:
        return False
    return common == base_abs


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        if not _is_within_directory(working_directory, full_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(full_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()

        if len(content) > MAX_FILE_CHARS:
            truncated = content[:MAX_FILE_CHARS]
            truncated += f'\n[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'
            return truncated
        return content
    except Exception as exc:
        return f"Error: {exc}"


# Function schema for tools API
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=(
        "Reads the contents of a file (truncated if too large) within the working directory."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "The path to the file, relative to the working directory."
                ),
            )
        },
    ),
)


