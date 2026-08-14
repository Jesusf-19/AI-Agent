# AI Agent

A Python-based AI coding agent project. The project uses the OpenAI SDK with OpenRouter and includes safe tool functions that allow the agent to inspect, read, write, and run files inside a controlled working directory.

The agent can receive a user prompt, decide which tool function to call, execute that function, add the result back into the conversation, and continue until it produces a final response. Also credit given to Boots.dev.

## Project Structure

```text
ai_agent/
├── calculator/
│   ├── main.py
│   ├── lorem.txt
│   ├── pkg/
│   │   ├── calculator.py
│   │   └── render.py
│   └── tests.py
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── call_function.py
├── config.py
├── main.py
├── test_get_files_info.py
├── test_get_file_content.py
├── test_write_file.py
├── test_run_python_file.py
├── pyproject.toml
├── uv.lock
└── README.md
```

## Features

* Sends user prompts to an LLM using the OpenAI SDK and OpenRouter
* Uses `argparse` to accept command-line prompts
* Supports a `--verbose` flag for printing prompt and token usage metadata
* Loads API keys from a `.env` file
* Includes safe file tools for listing, reading, writing, and running files
* Restricts file access to a permitted working directory
* Includes manual test files for each tool function
* Uses function schemas so the LLM knows which tools are available
* Runs in a loop so the agent can call tools and continue working until it has a final response

## Setup

Create a `.env` file in the project root:

```env
OPENROUTER_API_KEY=your_api_key_here
```

Install dependencies:

```bash
uv sync
```

Run the main program:

```bash
uv run main.py "Explain recursion in Python"
```

Run with verbose output:

```bash
uv run main.py --verbose "Explain recursion in Python"
```

## Main Script

The main script accepts a user prompt from the command line and sends it to the model.

The prompt is stored in a messages list:

```python
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]
```
The model is also given a list of available tools:
```python
response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions,
)
```
If the model asks to call a tool, the program runs the matching function and appends the result back into the conversation. The loop continues until the model returns a final response.

## Tool Functions

The `functions/` directory contains tools the agent can use to interact with the local project safely.

### `get_files_info`

Lists files and directories inside a target directory.

```python
get_files_info("calculator", ".")
```

Example output:

```text
- main.py: file_size=719 bytes, is_dir=False
- tests.py: file_size=1331 bytes, is_dir=False
- pkg: file_size=44 bytes, is_dir=True
```

### `get_file_content`

Reads the contents of a file while limiting the number of characters read.

The character limit is stored in `config.py`:

```python
MAX_CHARACTERS = 10000
```

If a file is too large, the output is truncated to avoid sending too much data to the LLM.

### `write_file`

Writes content to a file inside the permitted working directory.

```python
write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
```

Example success message:

```text
Successfully wrote to "pkg/morelorem.txt" (26 characters written)
```

### `run_python_file`

Runs a Python file inside the permitted working directory using `subprocess`.

```python
run_python_file("calculator", "main.py", ["3 + 5"])
```

It captures `stdout`, `stderr`, and prevents long-running scripts with a timeout.

## Function Calling

Each tool has a schema that describes how the LLM should call it. These schemas include the function name, description, and parameters.

The schemas are collected in available_functions and passed to the model.

The LLM does not receive the working_directory argument. Instead, the program injects it automatically:
```python
function_args["working_directory"] = "./calculator"
```
This keeps the agent limited to the calculator project and prevents it from accessing files outside the allowed directory.

## Agent Loop

The agent runs inside a loop with a maximum number of iterations.

Each loop:

Sends the current conversation history to the model
Checks if the model requested any tool calls
Runs the requested tool functions
Appends the tool results back into the message history
Continues until the model produces a final response

This allows the agent to inspect files, read code, run tests, write files, and answer based on the results.

## Path Safety

All tool functions validate paths before reading, writing, listing, or running files.

They use:

```python
os.path.abspath()
os.path.join()
os.path.normpath()
os.path.commonpath()
```

This prevents paths like this from accessing files outside the allowed directory:

```python
get_file_content("calculator", "../main.py")
```

If a path is outside the working directory, the function returns an error string instead of raising an exception.

## Manual Tests

Run the test files from the project root:

```bash
uv run test_get_files_info.py
uv run test_get_file_content.py
uv run test_write_file.py
uv run test_run_python_file.py
```

These tests check the file tools with valid inputs, invalid paths, missing files, and non-Python files.

## Technologies Used

* Python
* OpenAI SDK
* OpenRouter
* argparse
* python-dotenv
* subprocess
* JSON tool schemas
* uv

## What I Learned

This project helped me practice:

* Building command-line programs with `argparse`
* Using optional flags like `--verbose`
* Calling an LLM through the OpenAI SDK
* Loading API keys from environment variables
* Validating file paths safely
* Reading and writing files with Python
* Running Python scripts through subprocesses
* Creating manual test files for debugging
* Creating JSON schemas for tool/function calling
* Building an agent loop that can call tools and continue working

## Status

This project now includes a working AI agent loop. The agent can receive a prompt, request tool calls, execute local functions safely, add tool results back into the conversation, and continue until it produces a final response.
