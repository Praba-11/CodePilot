"""
Test runner for CodePilot functionality.

Tests file operations and code execution.
"""

import logging
from functions.write_file import write_file
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file

logger = logging.getLogger(__name__)


def main() -> None:
    """Run tests on function toolkit."""
    print("Testing CodePilot functions...")
    
    try:
        # Test run_python_file with calculator
        print("\n1. Running calculator without args:")
        result1 = run_python_file("calculator", "main.py")
        print(result1)

        print("\n2. Running calculator with expression '3 + 5':")
        result2 = run_python_file("calculator", "main.py", ["3 + 5"])
        print(result2)

        print("\n3. Running calculator tests:")
        result3 = run_python_file("calculator", "tests.py")
        print(result3)

        print("\n4. Attempting to access parent directory (should fail):")
        result4 = run_python_file("calculator", "../main.py")
        print(result4)

        print("\n5. Attempting to access nonexistent file (should fail):")
        result5 = run_python_file("calculator", "nonexistent.py")
        print(result5)
        
        print("\n✅ All tests completed successfully!")
    except Exception as exc:
        logger.error(f"Test execution failed: {exc}")
        print(f"❌ Test failed: {exc}")


if __name__ == "__main__":
    main()


