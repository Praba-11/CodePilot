# Step-by-Step: How to Use CodePilot

This guide walks you through setting up and using CodePilot from scratch.

## ✅ Step 1: Prerequisites Check

Ensure you have:
- **Python 3.11+** installed
  ```bash
  python --version
  ```
  
- **uv package manager** installed
  ```bash
  uv --version
  ```
  If not installed: https://docs.astral.sh/uv/installation/

- **Google Gemini API Key**
  Get one free at: https://ai.google.dev/

---

## 🚀 Step 2: Project Setup

### 2.1 Clone the Repository
```bash
git clone https://github.com/Praba-11/CodePilot.git
cd CodePilot
```

### 2.2 Create Virtual Environment
```bash
# Create venv with uv
uv venv

# Activate it
# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

You should see `(.venv)` in your terminal prompt when activated.

### 2.3 Install Dependencies
```bash
# Sync dependencies from pyproject.toml
uv sync
```

Or if dependencies aren't locked:
```bash
uv add google-genai==1.12.1 python-dotenv==1.1.0
```

### 2.4 Configure API Key
Create a `.env` file in the project root:
```bash
echo GEMINI_API_KEY="your_actual_api_key_here" > .env
```

**⚠️ IMPORTANT**: 
- Never commit `.env` to version control
- It's already in `.gitignore`
- Keep your API key secret!

---

## 🧪 Step 3: Testing (Optional but Recommended)

### 3.1 Test the Calculator (No API Key Needed)
```bash
# Basic math
python calculator/main.py "3 + 5"

# Complex expression
python calculator/main.py "2 * 3 + 4 * 5"

# Show help
python calculator/main.py
```

Expected output:
```json
{
  "expression": "3 + 5",
  "result": 8
}
```

### 3.2 Run Calculator Unit Tests
```bash
python -m pytest calculator/tests.py -v
```

Should see 10 passing tests.

### 3.3 Run Integration Tests (Requires Dependencies)
```bash
python tests.py
```

Tests file operations with the agent toolkit.

---

## 💡 Step 4: Use CodePilot

### 4.1 Basic Usage

```bash
python main.py "your question here"
```

**Example:**
```bash
python main.py "How many Python files are in this project?"
```

### 4.2 Verbose Mode (See Token Usage)

Add `--verbose` to see API token consumption:
```bash
python main.py "What does calculator.py do?" --verbose
```

Output includes:
- Your prompt
- Prompt tokens used
- Response tokens used
- Function calls made

### 4.3 List Available Models
```bash
python main.py --list-models
```

Shows all Gemini models available with your API key.

---

## 📋 Step 5: Example Interactions

Here are real-world prompts you can try:

### Task 1: Understand the Project
```bash
python main.py "What files are in the functions directory?"

python main.py "Explain what calculator/main.py does"

python main.py "How many lines of code are in main.py?"
```

### Task 2: Run the Calculator
```bash
python main.py "Run calculator/main.py with the expression 10 * 2 + 5"

python main.py "Evaluate the mathematical expression 2 * 3 + 4 * 5 using the calculator"
```

### Task 3: Analyze Code
```bash
python main.py "What is the purpose of the _is_within_directory function?"

python main.py "How does the calculator handle operator precedence?"

python main.py "Explain the security features of CodePilot"
```

### Task 4: Complex Tasks
```bash
python main.py "Create a test case for division by zero in the calculator"

python main.py "What would happen if I tried to access files outside the working directory?"

python main.py "List all the test cases in calculator/tests.py and tell me which operations they cover"
```

---

## 🔍 Step 6: Understanding Responses

When you ask CodePilot a question, it will:

1. **Receive** your prompt
2. **Decide** which functions it needs to call (list files, read code, run tests, etc.)
3. **Execute** those functions safely within the sandbox
4. **Analyze** the results
5. **Generate** a response and display it

Example with `--verbose`:
```
User prompt: How many Python files are in this project?

[Function call: get_files_info(directory='.')]
[Function call: get_file_content(file_path='main.py')]
[... more function calls ...]

Prompt tokens: 245
Response tokens: 89

Response: There are 7 Python files in this project:
- main.py (179 lines)
- tests.py (25 lines)
- calculator/main.py (35 lines)
- ...
```

---

## 🛡️ Step 7: Security Safeguards

CodePilot has built-in protections:

### ✅ File Access Limits
- Can only read files **within the project directory**
- Cannot access files outside with `../` tricks
- Example blocked attempt:
  ```bash
  python main.py "Read the contents of ../../../etc/passwd"
  # Result: Error - path is outside permitted working directory
  ```

### ✅ File Size Limits
- Large files are truncated to 10,000 characters
- Prevents huge payloads to the AI model
- Configurable in `functions/config.py`

### ✅ Execution Timeouts
- Scripts limited to 30-second execution
- Prevents infinite loops
- Configurable in `functions/run_python_file.py`

### ✅ Type Safety
- All functions have type hints
- Better error messages
- IDE support for autocompletion

---

## 🐛 Step 8: Troubleshooting

### Issue: `GEMINI_API_KEY is not set`

**Solution**: Create `.env` file with your key
```bash
# Create the file
echo GEMINI_API_KEY="your_key_here" > .env

# Verify it was created
cat .env
```

### Issue: `ModuleNotFoundError: No module named 'google'`

**Solution**: Install dependencies
```bash
uv sync

# Or manually:
uv add google-genai==1.12.1 python-dotenv==1.1.0
```

### Issue: `uv: The term 'uv' is not recognized`

**Solution**: Install uv
```bash
# Windows (using pip):
pip install uv

# Or download from: https://docs.astral.sh/uv/installation/
```

### Issue: Tests fail with dependency errors

**Solution**: Ensure virtual environment is activated
```bash
# Check if activated (should see .venv prefix)
python --version

# If not, activate it:
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

### Issue: Timeout errors on responses

**Solution**: API might be slow or limit rates
```bash
# Try again with simpler prompt
python main.py "What files are in the root?"

# Check API key validity
python main.py --list-models
```

---

## 📚 Step 9: Learn More

Read the detailed documentation:

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - How CodePilot works internally
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute code
- **[README.md](README.md)** - Project overview

---

## 🎯 Step 10: Real-World Workflow

Here's how you might use CodePilot in practice:

### Scenario: Code Review
```bash
# 1. Ask about specific code
python main.py "What does the run_python_file function do?"

# 2. Ask about security
python main.py "Are there any security vulnerabilities in write_file?"

# 3. Ask about testing
python main.py "Run the calculator tests and tell me which ones pass"
```

### Scenario: Learning Project
```bash
# 1. Understand structure
python main.py "Give me an overview of the project structure"

# 2. Analyze dependencies
python main.py "What are the external dependencies and why are they needed?"

# 3. Try modifications
python main.py "Show me how to add a subtract function to the calculator"
```

### Scenario: Debugging
```bash
# 1. Identify issues
python main.py "Are there any error conditions not handled in calculator.py?"

# 2. Test fixes
python main.py "Run calculator/tests.py and show me the results"

# 3. Verify solution
python main.py "Create and run a test for division by zero"
```

---

## ✨ Tips & Tricks

### Tip 1: Use Specific Prompts
❌ Bad: "What's this code?"  
✅ Good: "Explain the _is_within_directory() function and why it's important for security"

### Tip 2: Enable Verbose Mode for Learning
```bash
python main.py "How does the agent call functions?" --verbose
```

See exactly what functions are called and how.

### Tip 3: Build on Responses
You can ask follow-up questions that build on previous responses:

```bash
# First question
python main.py "How many test cases are in calculator/tests.py?"

# Follow-up
python main.py "What test cases are missing for the calculator?"

# Another follow-up
python main.py "Create new test cases for division edge cases"
```

### Tip 4: Check Token Usage
Use `--verbose` to see token counts. This helps estimate costs:
```bash
python main.py "Analyze the security of CodePilot" --verbose

# Shows: "Prompt tokens: 342" and "Response tokens: 156"
# Cost: (342 + 156) / 500,000 * 0.01 ≈ $0.000003 (roughly 0.003 cents)
```

### Tip 5: Create `.env` Variations
For different use cases, you can test with different API keys:
```bash
# Use with regular key
cat .env

# Backup current key
cp .env .env.backup

# Test with different key
echo GEMINI_API_KEY="different_key" > .env

# Restore original
cp .env.backup .env
```

---

## 🚀 You're Ready!

You now have a fully functional, production-ready AI coding assistant. 

**Next steps:**
1. Explore the code with various prompts
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand internals
3. Try extending it with new functions (see [CONTRIBUTING.md](CONTRIBUTING.md))
4. Use it for your own projects!

---

## 📞 Need Help?

- 📖 Check [ARCHITECTURE.md](ARCHITECTURE.md) for technical details
- 🤝 See [CONTRIBUTING.md](CONTRIBUTING.md) for development
- 💬 Review examples in this guide
- 📧 Check the README for additional resources

**Happy coding! 🎉**
