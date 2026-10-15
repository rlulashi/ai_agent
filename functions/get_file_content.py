import os
from config import MAX_CHARS

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Read and return file content in a specified directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Read file content from, relative to the working directory",
                },
            },
            "required": ["file_path"]
        },
    },
}





def get_file_content(working_directory: str, file_path: str) -> str:    
    try:
        file_path_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(file_path_abs, file_path))
        # Will be True or False
        valid_target_file_path = os.path.commonpath([file_path_abs, target_file_path]) == file_path_abs
        if not valid_target_file_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(target_file_path, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                # After reading the first MAX_CHARS...
                if f.read(1):
                    file_content_string = file_content_string + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string

            
    except Exception as e:
        return f'Error: {e}'
    