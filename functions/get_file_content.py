import os

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_directory = os.path.abspath(working_directory)
        working_path = os.path.abspath(os.path.join(working_directory, file_path))
        file_contents = ""
        with open(working_path, 'r') as rf:
            file_contents = rf.read(10_000)
            extra = rf.read(1)
            if extra:
                file_contents += f'[...File "{working_path}" truncated at 10000 characters]'
        return file_contents
    except Exception as e:
        return f'Error: {e}'
    
if __name__ == '__main__':
    print(get_file_content("./calculator", "main.py"))