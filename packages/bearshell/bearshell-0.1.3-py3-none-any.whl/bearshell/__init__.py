from datetime import datetime
import subprocess
import logging
import json
import shlex
from typing import List, Optional, Dict, Union

# Configure logging with local date and time
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class BearResponse:
    """Encapsulates the response from a BearShell command execution."""

    def __init__(self, start_time, end_time, stdout, stderr, error_message=None):
        self.start_time = start_time
        self.end_time = end_time
        self.stdout = stdout
        self.stderr = stderr
        self.error_message = error_message

    def to_dict(self) -> dict:
        """Converts the response to a dictionary."""
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "stdout": self.stdout,
            "stderr": self.stderr,
            "error_message": self.error_message
        }

    def to_json(self) -> str:
        """Converts the response to a JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class BearShell:
    """A secure shell executor that validates and runs commands with output streaming and safety checks."""

    def __init__(self, max_buffer_lines: int = 10000):
        """
        Initializes the BearShell executor.

        Args:
            max_buffer_lines (int): Maximum number of output lines to buffer before truncating.
        """
        self.allow_list = None
        self.block_list = None
        self.max_buffer_lines = max_buffer_lines
        self.command_presets = {}

    def set_allow_list(self, allowed_commands: List[str]):
        """Sets the allow-list of command names."""
        self.allow_list = set(allowed_commands)

    def set_block_list(self, blocked_commands: List[str]):
        """Sets the block-list of command names."""
        self.block_list = set(blocked_commands)

    def add_preset(self, name: str, command_template: List[str]):
        """
        Adds a named command preset.

        Args:
            name (str): The name of the preset.
            command_template (List[str]): A list of command parts, with placeholders in `{}`.
        """
        self.command_presets[name] = command_template

    def parse_command(self, command: Union[str, List[str]]) -> List[str]:
        """Parses a command string into a list if needed."""
        if isinstance(command, str):
            return shlex.split(command)
        return command

    def has_injection_risk(self, command_parts: List[str]) -> Optional[str]:
        """Checks for common shell injection tactics."""
        dangerous_patterns = [';', '&&', '|', '`', '$(', 'rm', 'shutdown', 'reboot']
        for part in command_parts:
            for pattern in dangerous_patterns:
                if pattern in part:
                    return f"Detected risky pattern: '{pattern}' in '{part}'"
        return None

    def check_policy(self, command_parts: List[str]) -> Optional[str]:
        """Checks against allow and block lists."""
        cmd = command_parts[0]
        if self.allow_list and cmd not in self.allow_list:
            return f"Command '{cmd}' not in allow-list."
        if self.block_list and cmd in self.block_list:
            return f"Command '{cmd}' is blocked by block-list."
        return None

    def run_preset(self, preset_name: str, **kwargs) -> BearResponse:
        """Runs a command from preset with substituted keyword arguments."""
        if preset_name not in self.command_presets:
            return BearResponse(datetime.now(), datetime.now(), '', '', f"Preset '{preset_name}' not found.")
        template = self.command_presets[preset_name]
        try:
            command = [part.format(**kwargs) for part in template]
        except KeyError as e:
            return BearResponse(datetime.now(), datetime.now(), '', '', f"Missing argument: {e}")
        return self.run(command)

    def run(self, command: Union[str, List[str]]) -> BearResponse:
        """
        Executes a command securely with output streaming and filtering.

        Args:
            command (Union[str, List[str]]): The command to run.

        Returns:
            BearResponse: The structured response of the command execution.
        """
        start_time = datetime.now()
        command_parts = self.parse_command(command)
        logging.info(f"Running command: {command_parts}")

        injection_risk = self.has_injection_risk(command_parts)
        if injection_risk:
            logging.warning(f"Blocked due to injection risk: {injection_risk}")
            return BearResponse(start_time, datetime.now(), '', '', injection_risk)

        policy_error = self.check_policy(command_parts)
        if policy_error:
            logging.warning(f"Blocked due to policy: {policy_error}")
            return BearResponse(start_time, datetime.now(), '', '', policy_error)

        try:
            process = subprocess.Popen(
                command_parts,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            stdout_lines = []
            stderr_lines = []
            for line in process.stdout:
                if len(stdout_lines) >= self.max_buffer_lines:
                    stdout_lines.append("[Truncated further output]")
                    process.kill()
                    break
                stdout_lines.append(line.rstrip())
            for line in process.stderr:
                if len(stderr_lines) >= self.max_buffer_lines:
                    stderr_lines.append("[Truncated further error output]")
                    break
                stderr_lines.append(line.rstrip())

            process.wait()
            end_time = datetime.now()
            return BearResponse(
                start_time,
                end_time,
                stdout='\n'.join(stdout_lines),
                stderr='\n'.join(stderr_lines)
            )
        except Exception as e:
            end_time = datetime.now()
            logging.exception("Execution failed.")
            return BearResponse(start_time, end_time, '', '', str(e))