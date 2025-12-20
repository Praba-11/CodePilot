"""
Output rendering for calculator results.

Formats expression results as JSON for consistent output.
"""

import json
from typing import Union


def format_json_output(
    expression: str, result: Union[int, float], indent: int = 2
) -> str:
    """Format expression and result as JSON.
    
    Args:
        expression: The evaluated expression.
        result: The numeric result.
        indent: JSON indentation level.
        
    Returns:
        JSON-formatted string with expression and result.
    """
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        result_to_dump = result

    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }
    return json.dumps(output_data, indent=indent)


