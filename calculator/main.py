"""
Simple expression calculator CLI.

Evaluates mathematical expressions with support for +, -, *, / operations
and proper operator precedence.
"""

import sys
import logging
from pkg.calculator import Calculator
from pkg.render import format_json_output

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    """Run the calculator CLI."""
    calculator = Calculator()
    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        return

    expression = " ".join(sys.argv[1:])
    try:
        result = calculator.evaluate(expression)
        if result is not None:
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            logger.warning("Expression is empty or contains only whitespace")
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        logger.error(f"Calculation error: {e}")
        print(f"Error: {e}")


if __name__ == "__main__":
    main()


