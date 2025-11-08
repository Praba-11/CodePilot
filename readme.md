# CodePilot

A CLI-based AI coding assistant that uses the Gemini (Google GenAI) API to iteratively inspect, edit, run, and test Python code inside a restricted project workspace. The agent exposes a small set of safe functions (list, read, write, execute) that the model can call to complete coding tasks while enforcing directory-boundary guardrails.

---

## Highlights

* CLI entrypoint that sends user prompts to Gemini and follows model-driven function calls to complete tasks.
* Secure function toolkit (implemented under `functions/`) with strict working-directory enforcement:

  * `get_files_info(working_directory, directory)` — list files and directories.
  * `get_file_content(working_directory, file_path)` — read file contents (with configurable truncation limit).
  * `write_file(working_directory, file_path, content)` — create/overwrite files safely.
  * `run_python_file(working_directory, file_path, args=[])` — execute Python files under a timeout, capturing stdout/stderr.
* Example subproject: `calculator/` with a small calculator app, tests, and utility renderers to exercise the agent.
* Uses a `system_prompt` and `types.FunctionDeclaration` / `types.Tool` to describe the available tools to the model so it plans function calls safely.

---

## Quick start

1. Initialize project and venv using the `uv` helper:

```bash
uv init "CodePilot"
cd "CodePilot"
uv venv
# add venv to .gitignore
source .venv/bin/activate
```

2. Add dependencies (these appear in `pyproject.toml`):

```bash
uv add google-genai==1.12.1
uv add python-dotenv==1.1.0
```

3. Set your Gemini API key in a `.env` file at project root:

```
GEMINI_API_KEY="your_api_key_here"
```

4. Run the CLI with the `uv` runner (example):

```bash
uv run main.py "Why are episodes 7-9 so much worse than 1-6?"
```

Add `--verbose` after the prompt to get token and tooling debug output:

```bash
uv run main.py "What is the meaning of life?" --verbose
```

---

## How the agent works (high level)

1. On startup, `main.py` loads environment variables via `python-dotenv`, creates a `genai.Client(api_key=...)`, and prepares the user prompt as a `types.Content` message list.
2. A `system_prompt` instructs the model that it may call specific functions to inspect or edit the workspace.
3. Function schemas are declared with `types.FunctionDeclaration` and grouped into a `types.Tool` (the `available_functions`).
4. The model's responses are inspected for `.function_calls`; when the model calls a function the agent maps that call to the corresponding local function in `functions/`, executes it (with working-directory injection), and returns the string result back to the model as a follow-up message.
5. The loop repeats until the model returns a final textual response or an unrecoverable error occurs.

---

## Safety & guardrails

* All function implementations join the provided `working_directory` with the user's relative path and then verify the resulting absolute path **remains inside** the working directory. Attempts to access `../` or absolute paths outside the allowed tree return an error string (e.g., `Error: Cannot list "../" as it is outside the permitted working directory`).
* File content reads are truncated to a configured maximum (stored in `config.py`) to avoid sending huge payloads to the model.
* Executions via `run_python_file` use `subprocess.run` with a 30s timeout and capture stdout/stderr; non-zero exit codes and exceptions are surfaced as structured strings so the model can react.

---

## Example interactions

* "what files are in the root?" → `get_files_info({'directory': '.'})`
* "read the contents of main.py" → `get_file_content({'file_path': 'main.py'})`
* "run main.py" → `run_python_file({'file_path': 'main.py'})`
* "write 'hello' to main.txt" → `write_file({'file_path': 'main.txt', 'content': 'hello'})`

---

## Future improvements

* Add authentication/authorization for multi-user scenarios.
* Add richer result parsing and a dry-run mode for potentially destructive write operations.
* Add more concise prompt engineering for multi-step repairs and rollbacks.
