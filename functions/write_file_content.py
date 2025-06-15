import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_directory = os.path.abspath(working_directory)
        working_path = os.path.abspath(os.path.join(working_directory, file_path))

        if not working_path.startswith(working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(working_path) :
            return f'Error: "{file_path}" is a directory'
        else:
            if not os.path.exists(os.path.dirname(working_path)):
                os.makedirs(os.path.dirname(working_path))
            write_length = 0
            with open(working_path, 'w') as wf:
                write_length = wf.write(content)
            return f'Successfully wrote to "{file_path}" ({write_length} characters written)'
    except Exception as e:
        return f'Error: {e}'