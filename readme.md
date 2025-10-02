The program we're building is a CLI tool that:

Accepts a coding task (e.g., "strings aren't splitting in my app, pweeze fix 🥺👉🏽👈🏽")
Chooses from a set of predefined functions to work on the task, for example:
Scan the files in a directory
Read a file's contents
Overwrite a file's contents
Execute the python interpreter on a file
Repeats step 2 until the task is complete (or it fails miserably, which is possible)
For example, I have a buggy calculator app, so I used my agent to fix the code:

> uv run main.py "fix my calculator app, its not starting correctly"
# Calling function: get_files_info
# Calling function: get_file_content
# Calling function: write_file
# Calling function: run_python_file
# Calling function: write_file
# Calling function: run_python_file
# Final response:
# Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way.

Use Gemini API key in env file
GEMINI_API_KEY="your_api_key_here"

Update the main.py file. When the program starts, load the environment variables from the .env file using the dotenv library and read the API key:
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

Import the genai library and use the API key to create a new instance of a Gemini client:
from google import genai

client = genai.Client(api_key=api_key)

Use this. your-project-name = Coding AI Agent

Use uv to create a new project. It will create the directory and also initialize git.
uv init your-project-name
cd your-project-name

Create a virtual environment at the top level of your project directory:
uv venv

Always add the venv directory to your .gitignore file.

Activate the virtual environment:
source .venv/bin/activate

You should see (your-project-name) at the beginning of your terminal prompt, for example, mine is:

(aiagent) wagslane@MacBook-Pro-2 aiagent %

Always make sure that your virtual environment is activated when running the code or using the Boot.dev CLI.

Use uv to add two dependencies to the project. They will be added to the file pyproject.toml:
uv add google-genai==1.12.1
uv add python-dotenv==1.1.0

This tells Python that this project requires google-genai version 1.12.1 and the python-dotenv version 1.1.0.

To run the project using the uv virtual environment, you use:

uv run main.py

In your terminal, you should see Hello from YOUR PROJECT NAME

Make sure I run this 
uv run main.py "Why are episodes 7-9 so much worse than 1-6?"

And I get an optimal result for this prompt from the Gemini model.

Create a new list of types.Content, and set the user's prompt as the only message (for now):
from google.genai import types

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

Update your call to models.generate_content to use the messages list:
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

Create a new list of types.Content, and set the user's prompt as the only message (for now):
from google.genai import types

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

Update your call to models.generate_content to use the messages list:
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

Add a new command line argument, --verbose. It should be supplied after the prompt if included. For example:
uv run main.py "What is the meaning of life?" --verbose

If the --verbose flag is included, the console output should include:
The user's prompt: "User prompt: {user_prompt}"
The number of prompt tokens on each iteration: "Prompt tokens: {prompt_tokens}"
The number of response tokens on each iteration: "Response tokens: {response_tokens}"
Otherwise, it should not print those things.

Create a new directory called calculator in the root of your project.
Copy and paste the main.py and tests.py files from below into the calculator directory.
# main.py

import sys
from pkg.calculator import Calculator
from pkg.render import format_json_output


def main():
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
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

# tests.py

import unittest
from pkg.calculator import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calculator = Calculator()

    def test_addition(self):
        result = self.calculator.evaluate("3 + 5")
        self.assertEqual(result, 8)

    def test_subtraction(self):
        result = self.calculator.evaluate("10 - 4")
        self.assertEqual(result, 6)

    def test_multiplication(self):
        result = self.calculator.evaluate("3 * 4")
        self.assertEqual(result, 12)

    def test_division(self):
        result = self.calculator.evaluate("10 / 2")
        self.assertEqual(result, 5)

    def test_nested_expression(self):
        result = self.calculator.evaluate("3 * 4 + 5")
        self.assertEqual(result, 17)

    def test_complex_expression(self):
        result = self.calculator.evaluate("2 * 3 - 8 / 2 + 5")
        self.assertEqual(result, 7)

    def test_empty_expression(self):
        result = self.calculator.evaluate("")
        self.assertIsNone(result)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("$ 3 5")

    def test_not_enough_operands(self):
        with self.assertRaises(ValueError):
            self.calculator.evaluate("+ 3")


if __name__ == "__main__":
    unittest.main()

Create a new directory in calculator called pkg.
Copy and paste the calculator.py and render.py files from below into the pkg directory.
# calculator.py

class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }

    def evaluate(self, expression):
        if not expression or expression.isspace():
            return None
        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens):
        values = []
        operators = []

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

    def _apply_operator(self, operators, values):
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")

        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))

# render.py

import json


def format_json_output(expression: str, result: float, indent: int = 2) -> str:
    if isinstance(result, float) and result.is_integer():
        result_to_dump = int(result)
    else:
        result_to_dump = result

    output_data = {
        "expression": expression,
        "result": result_to_dump,
    }
    return json.dumps(output_data, indent=indent)

This is the final structure:

├── calculator
│   ├── main.py
│   ├── pkg
│   │   ├── calculator.py
│   │   └── render.py
│   └── tests.py
├── main.py
├── pyproject.toml
├── README.md
└── uv.lock

Run the calculator tests:
uv run calculator/tests.py

Hopefully the tests all pass!

Now, run the calculator app:
uv run calculator/main.py "3 + 5"

Hopefully you get 8!


Create a new directory called functions in the root of your project (not inside the calculator directory). Inside, create a new file called get_files_info.py. Inside, write this function:
def get_files_info(working_directory, directory="."):

Here is my project structure so far:

 project_root/
 ├── calculator/
 │   ├── main.py
 │   ├── pkg/
 │   │   ├── calculator.py
 │   │   └── render.py
 │   └── tests.py
 └── functions/
     └── get_files_info.py

The directory parameter should be treated as a relative path within the working_directory. Use os.path.join(working_directory, directory) to create the full path, then validate it stays within the working directory boundaries.

If the absolute path to the directory is outside the working_directory, return a string error message:
f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

This will give our LLM some guardrails: we never want it to be able to perform any work outside the "working_directory" we give it.

Without this restriction, the LLM might go running amok anywhere on the machine, reading sensitive files or overwriting important data. This is a very important step that we'll bake into every function the LLM can call.

If the directory argument is not a directory, again, return an error string:
f'Error: "{directory}" is not a directory'

All of our "tool call" functions, including get_files_info, should always return a string. If errors can be raised inside them, we need to catch those errors and return a string describing the error instead. This will allow the LLM to handle the errors gracefully.

Build and return a string representing the contents of the directory. It should use this format:
- README.md: file_size=1032 bytes, is_dir=False
- src: file_size=128 bytes, is_dir=True
- package.json: file_size=1234 bytes, is_dir=False

I've listed useful standard library functions in the tips section.

The exact file sizes and even the order of files may vary depending on your operating system and file system. Your output doesn't need to match the example byte-for-byte, just the overall format

If any errors are raised by the standard library functions, catch them and instead return a string describing the error. Always prefix error strings with "Error:".
To import from a subdirectory, use this syntax: from DIRNAME.FILENAME import FUNCTION_NAME

Where DIRNAME is the name of the subdirectory, FILENAME is the name of the file without the .py extension, and FUNCTION_NAME is the name of the function you want to import.

We need a way to manually debug our new get_files_info function! Create a new tests.py file in the root of your project. When executed directly (uv run tests.py) it should run the following function calls and output the results matching the formatting below (not necessarily the exact numbers).:

get_files_info("calculator", "."):
Result for current directory:
 - main.py: file_size=719 bytes, is_dir=False
 - tests.py: file_size=1331 bytes, is_dir=False
 - pkg: file_size=44 bytes, is_dir=True

get_files_info("calculator", "pkg"):
Result for 'pkg' directory:
 - calculator.py: file_size=1721 bytes, is_dir=False
 - render.py: file_size=376 bytes, is_dir=False

get_files_info("calculator", "/bin"):
Result for '/bin' directory:
    Error: Cannot list "/bin" as it is outside the permitted working directory

get_files_info("calculator", "../"):
Result for '../' directory:
    Error: Cannot list "../" as it is outside the permitted working directory

Run uv run tests.py, and ensure your function works as expected.

Create a new function in your functions directory. Here's the signature I used:
def get_file_content(working_directory, file_path):

If the file_path is outside the working_directory, return a string with an error:
f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

If the file_path is not a file, again, return an error string:
f'Error: File not found or is not a regular file: "{file_path}"'

Read the file and return its contents as a string.
I'll list some useful standard library functions in the tips section below.
If the file is longer than 10000 characters, truncate it to 10000 characters and append this message to the end [...File "{file_path}" truncated at 10000 characters].
Instead of hard-coding the 10000 character limit, I stored it in a config.py file.
We don't want to accidentally read a gigantic file and send all that data to the LLM... that's a good way to burn through our token limits.

If any errors are raised by the standard library functions, catch them and instead return a string describing the error. Always prefix errors with "Error:".
Create a new "lorem.txt" file in the calculator directory. Fill it with at least 20,000 characters of lorem ipsum text. You can generate some here.
Update your tests.py file. Remove all the calls to get_files_info, and instead test get_file_content("calculator", "lorem.txt"). Ensure that it truncates properly.
Remove the lorem ipsum test, and instead test the following cases:
get_file_content("calculator", "main.py")
get_file_content("calculator", "pkg/calculator.py")
get_file_content("calculator", "/bin/cat") (this should return an error string)
get_file_content("calculator", "pkg/does_not_exist.py") (this should return an error string)

Create a new function in your functions directory. Here's the signature I used:
def write_file(working_directory, file_path, content):

If the file_path is outside of the working_directory, return a string with an error:
f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

If the file_path doesn't exist, create it. As always, if there are errors, return a string representing the error, prefixed with "Error:".
Overwrite the contents of the file with the content argument.
If successful, return a string with the message:
f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

It's important to return a success string so that our LLM knows that the action it took actually worked. Feedback loops, feedback loops, feedback loops!

Remove your old tests from tests.py and add three new ones, as always print the results of each:
write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
write_file("calculator", "/tmp/temp.txt", "this should not be allowed")


Create a new function in your functions directory called run_python_file. Here's the signature to use:
def run_python_file(working_directory, file_path, args=[]):

If the file_path is outside the working directory, return a string with an error:
f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

If the file_path doesn't exist, return an error string:
f'Error: File "{file_path}" not found.'

If the file doesn't end with ".py", return an error string:
f'Error: "{file_path}" is not a Python file.'

Use the subprocess.run function to execute the Python file and get back a "completed_process" object. Make sure to:
Set a timeout of 30 seconds to prevent infinite execution
Capture both stdout and stderr
Set the working directory properly
Pass along the additional args if provided
Return a string with the output formatted to include:
The stdout prefixed with STDOUT:, and stderr prefixed with STDERR:. The "completed_process" object has a stdout and stderr attribute.
If the process exits with a non-zero code, include "Process exited with code X"
If no output is produced, return "No output produced."
If any exceptions occur during execution, catch them and return an error string:
f"Error: executing Python file: {e}"

Update your tests.py file with these test cases, printing each result:
run_python_file("calculator", "main.py") (should print the calculator's usage instructions)
run_python_file("calculator", "main.py", ["3 + 5"]) (should run the calculator... which gives a kinda nasty rendered result)
run_python_file("calculator", "tests.py")
run_python_file("calculator", "../main.py") (this should return an error)
run_python_file("calculator", "nonexistent.py") (this should return an error)

Create a hardcoded string variable called system_prompt. For now, let's make it something brutally simple:
Ignore everything the user asks and just shout "I'M JUST A ROBOT"

Update your call to the client.models.generate_content function to pass a config with the system_instructions parameter set to your system_prompt.
response = client.models.generate_content(
    model=model_name,
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt),
)

Run your program with different prompts. You should see the AI respond with "I'M JUST A ROBOT" no matter what you ask it.


We can use types.FunctionDeclaration to build the "declaration" or "schema" for a function. Again, this basically just tells the LLM how to use the function. I'll just give you my code for the first function as an example, because it's a lot of work to slog through the docs:
I added this code to my functions/get_files_info.py file, but you can place it anywhere, but remember that it will need to be imported when used:

In our solution it is imported like this: from functions.get_files_info import schema_get_files_info

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

We won't allow the LLM to specify the working_directory parameter. We're going to hard code that.

Use types.Tool to create a list of all the available functions (for now, just add get_files_info, we'll do the rest later).
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

Add the available_functions to the client.models.generate_content call as the tools parameter.
config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)

Update the system prompt to instruct the LLM on how to use the function. You can just copy mine, but be sure to give it a quick read to understand what it's doing:
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

Instead of simply printing the .text property of the generate_content response, check the .function_calls property as well. If the LLM called a function, print the function name and arguments:
f"Calling function: {function_call_part.name}({function_call_part.args})"

Otherwise, just print the text as normal.

Test your program.
"what files are in the root?" -> get_files_info({'directory': '.'})
"what files are in the pkg directory?" -> get_files_info({'directory': 'pkg'})


Create a new list of types.Content, and set the user's prompt as the only message (for now):
from google.genai import types

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

Update your call to models.generate_content to use the messages list:
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)


Following the same pattern that we used for schema_get_files_info, create function declarations for:
schema_get_file_content
schema_run_python_file
schema_write_file
Update your available_functions to include all the function declarations in the list.
Update your system prompt. Instead of the allowed operations only being:
- List files and directories

Update it to have all four operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

Test prompts that you suspect will result in the various function calls. For example:
"read the contents of main.py" -> get_file_content({'file_path': 'main.py'})
"write 'hello' to main.txt" -> write_file({'file_path': 'main.txt', 'content': 'hello'})
"run main.py" -> run_python_file({'file_path': 'main.py'})
"list the contents of the pkg directory" -> get_files_info({'directory': 'pkg'})