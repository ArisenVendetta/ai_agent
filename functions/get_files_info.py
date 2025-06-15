import os

def get_files_info(working_directory, directory = None) -> str:
    try:
        if directory is None:
            directory = "."
        working_directory = os.path.abspath(working_directory)
        working_path = os.path.abspath(os.path.join(working_directory, directory))

        if not working_path.startswith(working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(working_path) :
            return f'Error: "{directory}" is not a directory'
        else:
            contents = os.listdir(working_path)
            output = []
            for item in contents:
                item_path = os.path.join(working_path, item)
                file_size = os.path.getsize(item_path)
                is_dir = os.path.isdir(item_path)
                output.append(f'{item}: file_size={file_size} bytes, is_dir={is_dir}')
            return '\n'.join(output)
    except Exception as e: 
        return f'Error: {e}'

    
if __name__ == '__main__':
    print(get_files_info("./", "calculator"))