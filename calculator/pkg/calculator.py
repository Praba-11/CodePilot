"""
Core calculator logic for expression evaluation.

Implements a shunting-yard algorithm for handling operator precedence
and evaluating mathematical expressions.
"""

from typing import Callable, Optional, Dict


class Calculator:
    """Evaluates mathematical expressions with proper operator precedence."""

    def __init__(self) -> None:
        """Initialize the calculator with supported operators and precedence."""
        self.operators: Dict[str, Callable[[float, float], float]] = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence: Dict[str, int] = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression: str) -> Optional[float]:
        """Evaluate a mathematical expression.
        
        Args:
            expression: A space-separated mathematical expression (e.g., "3 + 5 * 2").
            
        Returns:
            The result of the expression, or None if empty.
            
        Raises:
            ValueError: If the expression is invalid.
        """
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens: list) -> float:
        """Evaluate using the shunting-yard algorithm.
        
        Args:
            tokens: List of tokenized expression elements.
            
        Returns:
            The computed result.
            
        Raises:
            ValueError: If the expression structure is invalid.
        """
        values: list = []
        operators: list = []

        for token in tokens:
            if token in self.operators:
                while (
                    operators
                    and operators[-1] in self.operators
                    and self.precedence[operators[-1]] >= self.precedence[token]
                ):
                    self._apply_operator(operators, values)
                operators.append(token)
            else:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")

        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")

        return values[0]

    def _apply_operator(self, operators: list, values: list) -> None:
        """Apply the most recent operator to the values stack.
        
        Args:
            operators: Stack of operators.
            values: Stack of numeric values.
            
        Raises:
            ValueError: If there are insufficient operands.
        """
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))


