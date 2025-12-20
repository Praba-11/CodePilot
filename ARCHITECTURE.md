# CodePilot Architecture

This document describes the high-level architecture and design of CodePilot.

## Overview

CodePilot is a **CLI-based AI coding assistant** that uses the **Google Gemini API** to help with code inspection, modification, and execution within a **sandboxed project workspace**.

The system follows a secure **agent pattern** where:
1. User sends a prompt via CLI
2. AI model receives the prompt and available tools
3. Model calls functions to inspect/modify/execute code
4. Results are fed back to the model for iterative problem-solving
5. Final response is returned to user

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User (CLI)                          │
│              python main.py "prompt"                    │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   main.py (CLI Handler)                 │
│  - Parses arguments                                     │
│  - Loads environment variables                          │
│  - Manages logging                                      │
└────────────────────────┬────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────┐
│            Gemini API Client (genai.Client)             │
│  - Sends prompt + available functions to API            │
│  - Handles token counting                               │
│  - Receives function call requests from model           │
└────────────────────────┬────────────────────────────────┘
                         │
           ┌─────────────┼─────────────┐
           │             │             │
           ▼             ▼             ▼
    ┌──────────────┬─────────────┬─────────────┐
    │ get_files    │ get_file    │ write_file  │
    │ _info()      │ _content()  │ ()          │
    │              │             │             │
    │ Lists files  │ Reads file  │ Creates/    │
    │ in dir       │ contents    │ overwrites  │
    │              │ (truncated) │ files       │
    └──────────────┴─────────────┴─────────────┘
           │             │             │
           └─────────────┼─────────────┘
                         │
                         ▼
    ┌──────────────────────────────────┐
    │   run_python_file()              │
    │                                  │
    │   Executes Python files in       │
    │   subprocess with:               │
    │   - 30s timeout                  │
    │   - stdout/stderr capture        │
    │   - working dir isolation        │
    └──────────────────────────────────┘
```

## Module Structure

### `main.py` - Entry Point
**Responsibility**: CLI interface and Gemini orchestration

- Parses command-line arguments
- Loads `.env` for API credentials
- Configures logging
- Constructs system prompt with tool declarations
- Handles the agent loop with Gemini API
- Displays token usage when verbose mode enabled

**Key Functions**:
- `get_env_api_key()`: Load API key from environment
- `generate_gemini_response()`: Main orchestration function
- `count_prompt_tokens()`: Token counting (for cost/performance tracking)
- `extract_response_token_counts()`: Parse usage metadata from responses
- `main()`: CLI entry point

### `functions/` - Secure Tool Implementations

All functions include:
- ✅ Security: Directory boundary checks
- ✅ Type hints: Full type annotations
- ✅ Documentation: Comprehensive docstrings
- ✅ Error handling: Meaningful error messages
- ✅ Logging: Integration-ready

#### `get_files_info.py`
Lists files in a directory with metadata (size, type).

**Safety**: Validates that target directory is within working directory.

**API Schema**: Exposed as `schema_get_files_info` for Gemini function declarations.

#### `get_file_content.py`
Reads file contents with optional truncation (10,000 chars max).

**Safety**: 
- Directory boundary check
- File existence validation
- Truncation to prevent token overflow

**Config**: `MAX_FILE_CHARS` defined in `config.py`

#### `write_file.py`
Creates or overwrites files safely.

**Safety**:
- Directory boundary check
- Auto-creates parent directories
- Returns confirmation with character count

#### `run_python_file.py`
Executes Python scripts with isolation and timeout.

**Safety**:
- Directory boundary check
- File type validation (`.py` only)
- 30-second execution timeout
- Subprocess output capture (stdout/stderr)

**Error Handling**: 
- Timeout detection
- Exit code surfacing
- Exception wrapping

### `calculator/` - Example Subproject

Demonstrates the agent's capabilities with a simple calculator.

#### `calculator/pkg/calculator.py`
Expression evaluator using **shunting-yard algorithm**.

**Features**:
- Supports: `+`, `-`, `*`, `/`
- Proper operator precedence
- Full error validation

**Methods**:
- `evaluate(expression: str)`: Parse and compute result
- `_evaluate_infix()`: Core algorithm
- `_apply_operator()`: Stack-based operator application

#### `calculator/pkg/render.py`
JSON output formatting.

Converts results to JSON with proper integer/float handling.

#### `calculator/main.py`
CLI entry point for the calculator.

#### `calculator/tests.py`
Comprehensive unit tests (10 test cases covering all operations).

## Security Model

### Directory Boundary Enforcement

All file operations use `_is_within_directory()` validation:

```python
def _is_within_directory(base: str, target: str) -> bool:
    """Ensure target is within base directory."""
    base_abs = os.path.abspath(base)
    target_abs = os.path.abspath(target)
    common = os.path.commonpath([base_abs, target_abs])
    return common == base_abs
```

**Prevents**:
- `../` path traversal attacks
- Absolute path access outside working directory
- Symlink escapes

### Timeout Protection

Python execution uses 30-second timeout via `subprocess.run()`:
- Prevents infinite loops
- Protects against resource exhaustion

### Input Validation

All user-supplied paths are:
- Joined with working directory (relative paths only)
- Validated for directory boundary
- Checked for existence/type

## Data Flow Example: Running Calculator

```
User Input:
  python main.py 'What is 2 * 3 + 4?'

↓

Gemini receives:
  "What is 2 * 3 + 4?" + [get_files_info, get_file_content, 
                             write_file, run_python_file]

↓

Model decides: "I need to run calculator/main.py with args '2 * 3 + 4'"

↓

Agent calls:
  run_python_file("working_dir", "calculator/main.py", ["2", "*", "3", "+", "4"])

↓

Function execution:
  1. Validate working_dir boundary ✓
  2. Run: python calculator/main.py 2 * 3 + 4
  3. Capture output: {"expression": "2 * 3 + 4", "result": 10}

↓

Model receives output and formulates response:
  "The result of 2 * 3 + 4 is 10 (following order of operations)"

↓

Output returned to user
```

## Configuration

### Environment Variables

Required:
- `GEMINI_API_KEY`: Your Google Gemini API key

Optional:
- `UV_PATH`: Path to `uv` executable (auto-detected otherwise)

### Magic Numbers

Currently defined inline but should be configurable:

| Value | Location | Purpose |
|-------|----------|---------|
| `10000` | `functions/config.py` | Max file content chars |
| `30` | `functions/run_python_file.py` | Execution timeout (seconds) |
| `models/gemini-2.0-flash-001` | `main.py` | Default model |

## Testing Strategy

### Unit Tests
- `calculator/tests.py`: Calculator functionality (10 cases)
- Tests expressions, edge cases, error conditions

### Integration Tests
- `tests.py`: Toolkit function tests
- Tests file operations and code execution with security validation

### Manual Testing
```bash
# Test calculator
python calculator/main.py "3 + 5"

# Run unit tests
python -m pytest calculator/tests.py -v

# Run toolkit tests
python tests.py

# Test with Gemini (requires API key)
python main.py "What is the result of 10 / 2?"
```

## Future Improvements

### Proposed Enhancements
1. **Configuration file support** - Move magic numbers to `config.toml`
2. **Async Gemini calls** - Non-blocking API communication
3. **Function call persistence** - Log all function calls for audit trail
4. **Dry-run mode** - Preview function calls before execution
5. **Custom timeout profiles** - Different timeouts by file type
6. **Memory limits** - Restrict subprocess memory usage

### Multi-User Support
- Add authentication layer
- Isolate working directories per user
- Rate limiting on API calls
- Execution quotas

## Development Guidelines

### Adding New Tools

1. Create function in `functions/new_tool.py`
2. Include `_is_within_directory()` check
3. Define `schema_new_tool` for Gemini
4. Add to `functions/__init__.py`
5. Import in `main.py`
6. Add to function declarations in `generate_gemini_response()`
7. Test with `tests.py`

### Code Quality

- Type hints on all functions
- Docstrings (Google format)
- Error messages user-facing
- Logging at appropriate levels
- No print statements in libraries (use logging)

---

For more information, see:
- **README.md** - Quick start and usage
- **CONTRIBUTING.md** - Development guidelines
