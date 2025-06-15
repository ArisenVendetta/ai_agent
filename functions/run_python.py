import os
import subprocess

def run_python_file(working_directory: str, file_path: str, arguments: list[str] | None) -> str:
    try:
        if not arguments:
            arguments = []

        working_directory = os.path.abspath(working_directory)
        working_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not working_path.startswith(working_directory):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.exists(working_path):
            return f'Error: File "{file_path}" not found.'
        elif os.path.isdir(working_path) :
            return f'Error: "{file_path}" is a directory.'
        elif not working_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        else:
            result = subprocess.run(["python3", working_path] + arguments, cwd=working_directory, timeout=30, capture_output=True)
            stdout = f'STDOUT: {result.stdout.decode()}' if result.stdout else ''
            stderr = f'STDERR: {result.stderr.decode()}' if result.stderr else ''
            output = stdout if stdout else stderr
            if result.returncode != 0:
                output += f'\nProcess exited with code {result.returncode}'
            return output
    except Exception as e:
        return f'Error: executing Python file: {e}'