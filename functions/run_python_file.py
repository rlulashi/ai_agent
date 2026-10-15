import os
import subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs/executes python files in a specified directory relative to the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The Python file to execute, relative to the working directory",
                },
                 "args": {
                    "type": "array",
                    "items":{
                        "type": "string"
                    },
                    "description": "This generates an optional list of command line arguments to pass to the script",
                },
            },
            "required": ["file_path"]
        },
     },
}

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        file_path_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(file_path_abs, file_path))
        # Will be True or False
        valid_target_file_path = os.path.commonpath([file_path_abs, target_file_path]) == file_path_abs
        if not valid_target_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not target_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        else:
            command = ["python", target_file_path]
            if args:
                command.extend(args)
            cwd = file_path_abs
            result = subprocess.run(command, cwd=cwd, text=True, timeout=30 ,capture_output=True)
            output = []
            if result.returncode != 0:
                output.append(f"Process exited with code {result.returncode}")
            if not result.stdout and not result.stderr:
                output.append(f"No output produced")
            if result.stdout:
                output.append(f"STDOUT: {result.stdout}")
            if result.stderr:
                output.append(f"STDERR: {result.stderr}")
            return "\n".join(output)


    except Exception as e:
        return f"Error: executing Python file: {e}"
    