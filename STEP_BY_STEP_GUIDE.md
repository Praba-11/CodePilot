# 🎯 CodePilot: Step-by-Step Utilization & Testing Guide

## Overview
This guide provides a complete step-by-step approach to set up, understand, and test CodePilot from scratch.

---

## 📋 Part 1: Initial Setup (5 Minutes)

### Step 1.1: Verify Prerequisites
```bash
# Check Python version (need 3.11+)
python --version

# Check if uv is installed
uv --version

# If uv is missing, install it:
# Windows: pip install uv
# macOS/Linux: curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Step 1.2: Get API Key
1. Visit https://ai.google.dev/
2. Click "Get API Key"
3. Follow authentication steps
4. Copy your API key
5. Keep it secret!

### Step 1.3: Clone Repository
```bash
git clone https://github.com/Praba-11/CodePilot.git
cd CodePilot
```

### Step 1.4: Create Virtual Environment
```bash
# Create virtual environment
uv venv

# Activate it
# Windows:
.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate

# Verify (should see .venv prefix in prompt)
echo "Virtual env is now active"
```

### Step 1.5: Install Dependencies
```bash
# Install all dependencies
uv sync

# Or manually install:
uv add google-genai==1.12.1 python-dotenv==1.1.0
```

### Step 1.6: Configure API Key
```bash
# Create .env file with your key
# Windows (PowerShell):
@'
GEMINI_API_KEY="your_actual_key_here"
'@ | Out-File -Encoding UTF8 .env

# macOS/Linux:
echo 'GEMINI_API_KEY="your_actual_key_here"' > .env

# Verify it was created
cat .env
```

---

## 🧪 Part 2: Testing (10 Minutes)

### Step 2.1: Test Calculator (No API Key Needed)

```bash
# Test 1: Basic addition
python calculator/main.py "3 + 5"
# Expected: {"expression": "3 + 5", "result": 8}

# Test 2: Complex expression (tests operator precedence)
python calculator/main.py "2 * 3 + 4 * 5"
# Expected: {"expression": "2 * 3 + 4 * 5", "result": 26}

# Test 3: Single number
python calculator/main.py "42"
# Expected: {"expression": "42", "result": 42}

# Test 4: Help message
python calculator/main.py
# Expected: Shows usage instructions
```

### Step 2.2: Understand Calculator Output
```python
# Input: python calculator/main.py "10 / 2"
# Output:
{
  "expression": "10 / 2",
  "result": 5
}

# The output is JSON format:
# - "expression": Your input exactly as provided
# - "result": The computed result
#   - If integer result, shown as int (8 not 8.0)
#   - If decimal result, shown as float (2.5)
```

### Step 2.3: Run Calculator Unit Tests
```bash
# Run all tests
python -m pytest calculator/tests.py -v

# Expected output:
# ================================ test session starts =================================
# platform darwin -- Python 3.11.0, pytest-7.1.2, py-1.11.4 pluggy-0.19.0 -- ...
# collected 10 items
#
# calculator/tests.py::TestCalculator::test_addition PASSED                    [10%]
# calculator/tests.py::TestCalculator::test_subtraction PASSED                 [20%]
# calculator/tests.py::TestCalculator::test_multiplication PASSED              [30%]
# ... (more tests)
# =============================== 10 passed in 0.05s ==================================
```

### Step 2.4: Check Syntax
```bash
# Verify all Python files have valid syntax
python -m py_compile main.py
python -m py_compile tests.py
python -m py_compile calculator/main.py
python -m py_compile calculator/tests.py
python -m py_compile calculator/pkg/calculator.py
python -m py_compile calculator/pkg/render.py
python -m py_compile functions/get_files_info.py
python -m py_compile functions/get_file_content.py
python -m py_compile functions/write_file.py
python -m py_compile functions/run_python_file.py

# Or check all at once (Windows):
python -m py_compile main.py tests.py calculator/main.py functions/*.py

# If successful: No error messages
# If fails: Shows which file has syntax errors
```

---

## 🤖 Part 3: Basic API Testing (15 Minutes)

### Step 3.1: Test with Simple Queries

**Test 1: List Files**
```bash
python main.py "What files are in the root directory?"

# What happens:
# 1. Your prompt goes to Gemini
# 2. Gemini decides to call get_files_info()
# 3. Agent lists files in the project root
# 4. Gemini processes the list
# 5. Returns a natural language response

# Expected output:
# The root directory contains the following files:
# - main.py: main CLI entry point
# - tests.py: integration tests
# - pyproject.toml: project configuration
# - README.md: project documentation
# ... (more files)
```

**Test 2: Code Analysis**
```bash
python main.py "How many lines of code are in main.py?"

# What happens:
# 1. Gemini decides to call get_file_content()
# 2. Agent reads main.py (first 10,000 chars if > 10K)
# 3. Gemini counts lines
# 4. Returns count

# Expected output:
# The main.py file contains approximately 210 lines of code.
```

**Test 3: Run Calculator**
```bash
python main.py "Run the calculator with the expression 10 * 2 + 5"

# What happens:
# 1. Gemini decides to call run_python_file()
# 2. Agent executes: python calculator/main.py 10 * 2 + 5
# 3. Captures output: {"expression": "10 * 2 + 5", "result": 25}
# 4. Gemini explains result

# Expected output:
# The calculator evaluated "10 * 2 + 5" and got 25
# This follows the correct order of operations (multiplication before addition)
```

### Step 3.2: Enable Verbose Mode
```bash
# See token usage and function calls
python main.py "How many files are in this project?" --verbose

# Verbose output shows:
# User prompt: How many files are in this project?
# Calling function: get_files_info({'directory': '.'})
# Prompt tokens: 245
# Response tokens: 89
# [Response follows...]

# This is useful for:
# - Understanding what the AI is doing
# - Monitoring API usage and costs
# - Debugging issues
```

### Step 3.3: Test Help Functions
```bash
# Show CLI help
python main.py --help

# List available Gemini models
python main.py --list-models

# Activate with no arguments (shows greeting)
python main.py
```

---

## 🔍 Part 4: Advanced Testing (20 Minutes)

### Step 4.1: Security Testing

**Test 1: Directory Traversal Prevention**
```bash
# This SHOULD fail (for security)
python main.py "Read the contents of ../../../etc/passwd"

# Expected output:
# Error: Cannot read "../../../etc/passwd" as it is outside 
# the permitted working directory

# Why: CodePilot only allows reading files within the project
```

**Test 2: File Access Verification**
```bash
# This SHOULD work (file in project)
python main.py "What is the first line of main.py?"

# This SHOULD fail (outside project)
python main.py "What is the first line of /etc/hostname?"

# This demonstrates the directory boundary protection
```

### Step 4.2: Understanding Function Calls

```bash
python main.py "Show me the calculator code" --verbose

# Notice the function calls in verbose output:
# Calling function: get_file_content({'file_path': 'calculator/pkg/calculator.py'})

# Available functions (in verbose output):
# 1. get_files_info(directory) - List files
# 2. get_file_content(file_path) - Read file  
# 3. write_file(file_path, content) - Create/write file
# 4. run_python_file(file_path, args) - Execute Python

# These are the only operations the AI can do.
# No command execution, only Python files, within project boundary.
```

### Step 4.3: Timeout Testing

```bash
# Create a test file that runs for > 30 seconds
echo 'import time; time.sleep(35)' > test_timeout.py

# Try to run it
python main.py "Run test_timeout.py"

# Expected output:
# Error: Script execution timed out after 30 seconds

# This shows timeout protection is working
# Files are in:
rm test_timeout.py  # Clean up
```

---

## 📚 Part 5: Understanding How It Works (15 Minutes)

### Step 5.1: The Agent Loop

```
┌──────────────────────────────────────────────────┐
│ 1. YOU: "Run calculator with 5 + 3"             │
└────────────────────┬─────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│ 2. MAIN.PY: Sends prompt + function declarations│
│    to Gemini API                                 │
└────────────────────┬─────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│ 3. GEMINI: Analyzes prompt and available         │
│    functions. Decides: "I should call            │
│    run_python_file()"                           │
└────────────────────┬─────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│ 4. AGENT: Executes:                              │
│    run_python_file("calculator", "main.py",      │
│                     ["5", "+", "3"])             │
│                                                  │
│    With security checks:                         │
│    ✓ Is path within working directory?          │
│    ✓ Is it a .py file?                          │
│    ✓ Does file exist?                           │
└────────────────────┬─────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│ 5. SUBPROCESS: Runs:                             │
│    python calculator/main.py 5 + 3               │
│    (with 30s timeout)                            │
│                                                  │
│    Output:                                       │
│    {"expression": "5 + 3", "result": 8}         │
└────────────────────┬─────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│ 6. GEMINI: Receives output and formulates        │
│    natural language response:                    │
│    "The calculator evaluated 5 + 3 and          │
│     returned 8, which is correct."               │
└────────────────────┬─────────────────────────────┘
                     ↓
┌──────────────────────────────────────────────────┐
│ 7. OUTPUT: You see the response                  │
└──────────────────────────────────────────────────┘
```

### Step 5.2: Code Structure

```
main.py
├── get_env_api_key()           [Load API key from .env]
├── count_prompt_tokens()       [Count tokens for cost]
├── extract_response_token_counts() [Parse response stats]
├── generate_gemini_response()  [Main agent loop]
├── main()                      [CLI entry point]
└── if __name__ == "__main__": main()

functions/
├── get_files_info.py
│   └── List files in directory (with boundary check)
├── get_file_content.py
│   └── Read file contents (with truncation)
├── write_file.py
│   └── Write/create files (with boundary check)
└── run_python_file.py
    └── Execute Python scripts (with timeout)

calculator/
└── Simple math expression evaluator
    ├── Uses shunting-yard algorithm
    ├── Supports +, -, *, /
    ├── Respects operator precedence
    └── Includes 10 unit tests
```

### Step 5.3: Security Model

```
ALLOWED:
✅ Read files from project directory
✅ Write files to project directory
✅ Execute Python files in project directory
✅ Call supported functions with valid paths

NOT ALLOWED:
❌ Read files outside project (../, absolute paths)
❌ Execute non-Python files
❌ Read files > 10,000 characters (truncated)
❌ Run scripts > 30 seconds
❌ Execute arbitrary commands

VERIFIED:
✓ All paths validated with os.path.commonpath()
✓ All file operations use subprocess isolation
✓ All errors logged for audit trail
✓ Full type hints prevent injection
```

---

## 💡 Part 6: Real-World Examples (15 Minutes)

### Example 1: Understanding the Project

```bash
# Q1: What is the purpose of this project?
python main.py "What is CodePilot and what does it do?"

# Q2: How is it structured?
python main.py "Explain the directory structure of CodePilot"

# Q3: What are the security features?
python main.py "What security protections does CodePilot have?"

# Q4: How do I use it?
python main.py "How would I use this AI agent?"
```

### Example 2: Learning the Code

```bash
# Q1: Understanding a function
python main.py "What does the _is_within_directory function do?"

# Q2: How the calculator works
python main.py "Explain the shunting-yard algorithm used in calculator.py"

# Q3: Error handling
python main.py "Show me all the error checks in get_file_content.py"

# Q4: Testing
python main.py "What test cases does the calculator have?"
```

### Example 3: Code Tasks

```bash
# Q1: Run tests
python main.py "Run the calculator unit tests and summarize the results"

# Q2: Analyze code quality
python main.py "Are there any type hints missing in main.py?"

# Q3: Feature requests
python main.py "What would happen if I added a square root function to the calculator?"

# Q4: Security review
python main.py "Could someone use a symlink to read files outside the project?"
```

---

## 🔧 Part 7: Troubleshooting (10 Minutes)

### Issue 1: API Key Not Found
```bash
# Error: GEMINI_API_KEY is not set

# Solution:
# 1. Create .env file:
echo GEMINI_API_KEY="your_key_here" > .env

# 2. Verify it exists:
cat .env

# 3. Try again:
python main.py "test"
```

### Issue 2: Module Not Found
```bash
# Error: ModuleNotFoundError: No module named 'google'

# Solution:
# 1. Ensure venv is activated (see (.venv) in prompt)
# 2. Run: uv sync
# 3. Try again
```

### Issue 3: Calculator Not Working
```bash
# Error when running: python calculator/main.py "5 + 3"

# Solution:
# 1. Check Python version: python --version
# 2. Check file exists: ls calculator/main.py
# 3. Check syntax: python -m py_compile calculator/main.py
# 4. Run directly: python calculator/main.py 5 + 3
```

### Issue 4: Permission Denied
```bash
# Error: Permission denied

# On macOS/Linux:
chmod +x run.sh
chmod +x run.ps1

# Windows: Run command prompt as Administrator
```

---

## ✅ Part 8: Verification Checklist

Go through this checklist to verify everything works:

- [ ] Python 3.11+ installed (`python --version`)
- [ ] uv installed (`uv --version`)
- [ ] Repository cloned and in correct directory
- [ ] Virtual environment created (`uv venv`)
- [ ] Virtual environment activated (see `(.venv)` in prompt)
- [ ] Dependencies installed (`uv sync`)
- [ ] `.env` file created with API key
- [ ] Calculator test works: `python calculator/main.py "3 + 5"`
- [ ] Calculator tests pass: `python -m pytest calculator/tests.py`
- [ ] Syntax check passes: `python -m py_compile main.py tests.py`
- [ ] Simple query works: `python main.py "Hello"`
- [ ] Verbose mode works: `python main.py "test" --verbose`
- [ ] List models works: `python main.py --list-models`

If all checked: ✅ **CodePilot is ready to use!**

---

## 🚀 Part 9: Next Steps

### Learn More:
1. Read [USAGE.md](USAGE.md) - Complete usage guide
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) - How it works
3. Read [CONTRIBUTING.md](CONTRIBUTING.md) - Development guide

### Try More Examples:
```bash
# Code analysis
python main.py "Show me all functions in main.py with --verbose"

# Learning
python main.py "Teach me about how the calculator determines operator precedence"

# Complex tasks
python main.py "Create and run a test to verify calculator handles large numbers"

# Multi-step
python main.py "First, list all test files. Then explain what each one tests."
```

### Explore Features:
```bash
# Token monitoring
python main.py "complex query" --verbose  # See token usage and costs

# Model selection
python main.py --list-models  # See all available models

# Help
python main.py --help  # See all CLI options
```

---

## 📊 Quick Reference

### Commands
```bash
python main.py                              # Greeting
python main.py "your prompt"                # Ask a question
python main.py "prompt" --verbose           # With token info
python main.py --list-models                # Available models
python main.py --help                       # Show help
```

### Test Commands
```bash
python calculator/main.py "3 + 5"                      # Quick calc
python -m pytest calculator/tests.py -v                # Run tests
python tests.py                                         # Integration tests
python -m py_compile *.py calculator/*.py              # Syntax check
```

### Configuration
```bash
cat .env                           # View API key (should exist)
cat functions/config.py            # View max file size
cat functions/run_python_file.py   # View timeout value
```

---

## 🎉 You're All Set!

You now have:
- ✅ Working CodePilot installation
- ✅ Understanding of how it works
- ✅ Knowledge of security features
- ✅ Ability to test and verify functionality
- ✅ Reference for troubleshooting
- ✅ Pathways to learn more

**Happy exploring! 🚀**
