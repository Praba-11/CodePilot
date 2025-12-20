# Contributing to CodePilot

Thank you for your interest in contributing to CodePilot! We welcome contributions from the community. Please follow the guidelines below to help us maintain code quality and consistency.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/CodePilot.git
   cd CodePilot
   ```
3. **Create a virtual environment** and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style & Standards

### Python Code Standards
- Use **PEP 8** style guide
- Add **type hints** to all function parameters and returns
- Include **docstrings** for all functions and classes (Google-style format)
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Example Function Format
```python
def example_function(param1: str, param2: int) -> bool:
    """Brief description of what the function does.
    
    Longer description if needed, explaining behavior and edge cases.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
        
    Returns:
        Description of return value.
        
    Raises:
        ValueError: When validation fails.
    """
    pass
```

## Making Changes

1. **Write clear, descriptive commit messages**:
   ```bash
   git commit -m "feat: add new calculator function"
   git commit -m "fix: handle edge case in file validation"
   ```

2. **Keep commits atomic** - each commit should represent one logical change

3. **Add tests** for any new functionality:
   ```bash
   python -m pytest calculator/tests.py -v
   ```

4. **Run existing tests** to ensure nothing breaks:
   ```bash
   python tests.py
   python -m pytest calculator/tests.py
   ```

## Security Considerations

- **Never** commit `.env` files or API keys
- Always validate file paths against the working directory boundary
- Use subprocess with appropriate timeout limits
- Sanitize any user input before processing
- Review existing security checks in `functions/*.py`

## Testing Your Changes

Before submitting a pull request:

```bash
# Test the calculator module
python calculator/main.py "2 + 3 * 4"

# Run unit tests
python -m pytest calculator/tests.py -v

# Test the toolkit functions
python tests.py

# Check for syntax errors
python -m py_compile main.py tests.py calculator/main.py functions/*.py
```

## Submitting a Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request** with:
   - Clear title describing the change
   - Detailed description of what changed and why
   - Reference to any related issues (e.g., "Closes #42")
   - Evidence that tests pass

3. **Respond to feedback** - maintainers may request changes

## Reporting Bugs

Found a bug? Please create an issue with:
- **Title**: Clear, concise description
- **Description**: What happened vs. what you expected
- **Steps to reproduce**: How to recreate the issue
- **Environment**: Python version, OS, relevant tools
- **Example code**: Minimal reproducible example if applicable

## Feature Requests

Have an idea? Please open an issue with:
- **Title**: Feature description
- **Motivation**: Why this feature would be useful
- **Proposed implementation**: How you might implement it
- **Example usage**: How users would interact with it

## Code Review Process

All contributions go through code review. Reviewers will check for:
- ✅ Code quality and style compliance
- ✅ Type hints and documentation
- ✅ Test coverage
- ✅ Security concerns
- ✅ Performance implications

## Questions?

- Open a **GitHub Discussion**
- Check the **README.md** for architecture details
- Review **existing code** for patterns and conventions

## License

By contributing to CodePilot, you agree that your contributions will be licensed under the MIT License.

---

Thank you for helping make CodePilot better! 🚀
