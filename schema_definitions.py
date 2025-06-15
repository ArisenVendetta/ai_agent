from google.genai import types

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
        required=['directory']
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name='get_file_content',
    description='Reads up to the first 10,000 characters from specified file, constrained to the working directory',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='The path to the file, relative to the working directory.'
            )
        },
        required=['file_path']
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name='run_python_file',
    description='Runs Python files with optional arguments',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='The path to the python file to execute, relative to the working directory'
            ),
            'arguments': types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description='List of arguments provided to the python file'
            )
        },
        required=['file_path']
    )
)

schema_write_file = types.FunctionDeclaration(
    name='write_file',
    description='Writes (or overwrites if already exists) files with the provided content',
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            'file_path': types.Schema(
                type=types.Type.STRING,
                description='The path for where to write the file, relative to the working directory'
            ),
            'content': types.Schema(
                type=types.Type.STRING,
                description='The content to write to the file'
            )
        },
        required=['file_path', 'content']
    )
)

DEFINED_SCHEMAS = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
]