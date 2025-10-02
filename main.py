import os
import sys
import argparse
from typing import Optional, Tuple

from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file


def get_env_api_key() -> Optional[str]:
    load_dotenv()
    return os.environ.get("GEMINI_API_KEY")


def print_greeting() -> None:
    print("Hello from Coding AI Agent")


def count_prompt_tokens(client: genai.Client, model: str, messages: list) -> Optional[int]:
    try:
        ct = client.models.count_tokens(model=model, contents=messages)
        # Support different field names across SDK versions
        if hasattr(ct, "total_tokens"):
            return getattr(ct, "total_tokens")
        if hasattr(ct, "input_tokens"):
            return getattr(ct, "input_tokens")
        # Fallback to dict-like
        return ct.get("total_tokens") if isinstance(ct, dict) else None
    except Exception:
        return None


def extract_response_token_counts(response) -> Tuple[Optional[int], Optional[int]]:
    """Return (prompt_tokens, response_tokens) if available, else (None, None)."""
    usage = None
    for attr in ("usage_metadata", "usage"):
        if hasattr(response, attr):
            usage = getattr(response, attr)
            break
    if not usage:
        return None, None

    # Try common names across SDKs
    prompt_tokens = None
    response_tokens = None
    for name in ("prompt_token_count", "input_tokens", "prompt_tokens"):
        if hasattr(usage, name):
            prompt_tokens = getattr(usage, name)
            break
        if isinstance(usage, dict) and name in usage:
            prompt_tokens = usage[name]
            break
    for name in ("candidates_token_count", "output_tokens", "response_tokens"):
        if hasattr(usage, name):
            response_tokens = getattr(usage, name)
            break
        if isinstance(usage, dict) and name in usage:
            response_tokens = usage[name]
            break
    return prompt_tokens, response_tokens


def generate_gemini_response(prompt: str, api_key: str, verbose: bool = False) -> str:
    client = genai.Client(api_key=api_key)

    # Updated system prompt per README: instruct tool usage
    system_prompt = (
        """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
    ).strip()

    # Build messages per README
    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    if verbose:
        print(f"User prompt: {prompt}")

    model = "models/gemini-2.0-flash-001"
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
        ),
    )

    if verbose:
        # Prefer usage info from response; otherwise compute prompt tokens directly
        prompt_tokens, response_tokens = extract_response_token_counts(response)
        if prompt_tokens is None:
            prompt_tokens = count_prompt_tokens(client, model, messages)
        if prompt_tokens is not None:
            print(f"Prompt tokens: {prompt_tokens}")
        if response_tokens is not None:
            print(f"Response tokens: {response_tokens}")

    # If the model issued function calls, surface them
    try:
        for part in getattr(response, "function_calls", []) or []:
            print(f"Calling function: {part.name}({part.args})")
    except Exception:
        pass

    return getattr(response, "text", getattr(response, "output_text", str(response)))


def main() -> None:
    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument("prompt", nargs="?", help="User prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Print prompt and token counts")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    args = parser.parse_args()

    if args.list_models:
        api_key = get_env_api_key()
        if not api_key:
            print(
                "Error: GEMINI_API_KEY is not set. Create a .env with GEMINI_API_KEY=...",
                file=sys.stderr,
            )
            sys.exit(1)
        client = genai.Client(api_key=api_key)
        models = list(client.models.list())
        for m in models:
            model_name = getattr(m, "name", getattr(m, "id", str(m)))
            print(model_name)
        return

    # If no prompt, show greeting (setup verification)
    if not args.prompt:
        print_greeting()
        return

    prompt = args.prompt
    api_key = get_env_api_key()
    if not api_key:
        print(
            "Error: GEMINI_API_KEY is not set. Create a .env with GEMINI_API_KEY=...",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        output = generate_gemini_response(prompt, api_key, verbose=args.verbose)
        print(output)
    except Exception as exc:  # noqa: BLE001 - top-level boundary
        print(f"Gemini request failed: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()


