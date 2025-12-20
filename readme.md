# CodePilot

> An AI-powered coding assistant that uses Google Gemini API to iteratively inspect, edit, run, and test Python code in a sandboxed workspace.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)

## Overview

CodePilot is a **CLI-based AI coding assistant** that uses the Gemini (Google GenAI) API to iteratively inspect, edit, run, and test Python code inside a restricted project workspace.

### Key Features

- 🤖 **AI-Powered**: Leverage Google Gemini 2.0 Flash for intelligent code understanding
- 🔒 **Secure Sandbox**: Directory boundary enforcement prevents path traversal attacks
- ⚡ **Fast Execution**: 30-second timeout with output capture
- 📦 **Type-Safe**: Full type hints for IDE support
- 📝 **Well-Documented**: Comprehensive guides and docstrings
- 🧪 **Tested**: Example calculator with 10+ unit tests

## Quick Start

### Prerequisites
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- [Google Gemini API key](https://ai.google.dev/)

### Installation

```bash
# Clone repository
git clone https://github.com/Praba-11/CodePilot.git
cd CodePilot

# Create virtual environment
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
uv sync

# Create .env file with your API key
echo 'GEMINI_API_KEY="your_key_here"' > .env
```

### Usage Examples

```bash
# Simple query
python main.py "How many lines of code are in main.py?"

# Run the calculator
python main.py "Run calculator/main.py with 10 * 2 + 5"

# Verbose mode (shows token usage)
python main.py "What does calculator.py do?" --verbose
```

## How It Works

**Agent Pattern:**
1. User provides prompt via CLI
2. Prompt + function declarations → Gemini API
3. Model decides which functions to call
4. Agent executes with security checks
5. Results fed back to model
6. Final response returned to user

### Available Functions

| Function | Purpose | Security |
|----------|---------|----------|
| `get_files_info()` | List files | Directory boundary check |
| `get_file_content()` | Read files | Boundary + 10K char truncation |
| `write_file()` | Create/update files | Boundary + auto parent dirs |
| `run_python_file()` | Execute scripts | Boundary + 30s timeout |

## Security

✅ **Directory Boundary** - Prevents `../` path traversal  
✅ **Output Truncation** - Limits file content to 10,000 chars  
✅ **Execution Timeout** - Scripts limited to 30 seconds  
✅ **Type Safety** - Full type hints throughout  

## Project Structure

```
CodePilot/
├── main.py               # CLI entry point
├── tests.py             # Integration tests
├── LICENSE              # MIT
├── README.md            # This file
├── CONTRIBUTING.md      # Development guide
├── ARCHITECTURE.md      # Technical details
├── functions/           # Safe tool implementations
└── calculator/          # Example subproject
```

## Example: Calculator

```bash
python calculator/main.py "3 + 5"
# Output: {"expression": "3 + 5", "result": 8}

python -m pytest calculator/tests.py -v  # Run tests
```

## Testing

```bash
# Unit tests
python -m pytest calculator/tests.py -v

# Integration tests
python tests.py

# Syntax check
python -m py_compile main.py tests.py calculator/main.py functions/*.py
```

## Configuration

Create a `.env` file:
```env
GEMINI_API_KEY="your_key_here"
```

Adjust in `functions/config.py`:
```python
MAX_FILE_CHARS = 10000
```

Adjust in `functions/run_python_file.py`:
```python
EXECUTION_TIMEOUT_SECONDS = 30
```

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style (PEP 8, type hints, docstrings)
- How to submit PRs
- Testing requirements

See [ARCHITECTURE.md](ARCHITECTURE.md) for:
- System design and data flow
- Security model details
- How to add new tools

## License

MIT - See [LICENSE](LICENSE)

## Author

**Praba-11** - [GitHub](https://github.com/Praba-11)

---

**Happy coding! 🚀**
