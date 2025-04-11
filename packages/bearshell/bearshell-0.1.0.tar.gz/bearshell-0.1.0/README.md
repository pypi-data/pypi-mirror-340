# BearShell
A (relatively) secure and easy-to-use subprocess implementation for Python

<img src="img/bearshell.png" alt="BearShell" width="400"/>

`BearShell` is a Python class for executing shell commands securely with output streaming, injection risk protection, and support for command presets. This tool provides an easy-to-use interface while enforcing security policies and offering control over the commands executed.

## Features
- **Secure Command Execution**: Protects against common shell injection tactics.
- **Command Presets**: Allows predefined command templates with substitution.
- **Output Streaming**: Streams output line-by-line while capturing the entire result.
- **Allow-List and Block-List**: Policies to restrict which commands can or cannot be executed.
- **Injection Risk Detection**: Detects risky shell patterns like `;`, `&&`, `rm`, and others.

## Installation

1. Clone the repository or install the class directly into your project.
2. No dependencies outside the standard Python library.

## Example Usage

```python
from bearshell import BearShell

# Create BearShell object with a buffer limit of 5000 lines
shell = BearShell(max_buffer_lines=5000)

# Set allow-list of safe commands
shell.set_allow_list(["searchsploit", "nmap"])

# Set block-list of risky commands
shell.set_block_list(["rm", "shutdown"])

# Define a preset command for running searchsploit
shell.add_preset("search_exploit", ["searchsploit", "{query}"])

# Run the search_exploit preset with a query
response = shell.run_preset("search_exploit", query="apache")

# Output the response as a dictionary
print(response.to_dict())

# Run a custom command directly (this will be parsed and validated)
response = shell.run("nmap -p 80 192.168.1.1")

# Output the response
print(response.to_dict())

# Run a custom command directly (this will be parsed and validated)
response = shell.run("nmap -p 80 192.168.1.1")

# Output the response
print(response.to_dict())
```

## Command Response
### The BearResponse returned by the run and run_preset methods contains:

`start_time` Time when the command started.

`end_time` Time when the command finished.

`stdout` Standard output (captured during the command execution).

`stderr` Standard error output.

`error_message` An error message in case of a failure (e.g., injection risk or policy violation).

### You can get the response in various formats:

Dictionary: `response.to_dict()`

JSON: `response.to_json()`

### Policy Enforcement
Allow-List: Only allows commands listed in the allow-list to run.

Block-List: Blocks commands that are added to the block-list.

Injection Risk Detection: Automatically checks for dangerous patterns (e.g., rm, shutdown) and blocks commands with such patterns.

### Example Response Object

{
  "start_time": "2025-04-10T12:30:00",
  "end_time": "2025-04-10T12:30:05",
  "stdout": "Found exploit for Apache\n",
  "stderr": "",
  "error_message": null
}