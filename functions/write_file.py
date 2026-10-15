import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites files in a specified directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File being written or overwritten on, relative to the working directory",
                },
                 "content": {
                    "type": "string",
                    "description": "The text to write into the file",
                    },
            },
            "required": ["file_path", "content"]
        },
     },
}



def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        file_path_abs = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(file_path_abs, file_path))
        # Will be True or False
        valid_target_file_path = os.path.commonpath([file_path_abs, target_file_path]) == file_path_abs
        if not valid_target_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        else:
            os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
            with open(target_file_path, "w") as f:
                f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
            
    except Exception as e:
        return f'Error: {e}'
    
