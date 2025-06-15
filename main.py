import os, sys
from typing import Callable, Sequence
from pprint import pprint

from dotenv import load_dotenv
from google import genai
from google.genai import types

from schema_definitions import DEFINED_SCHEMAS
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file_content import write_file
from functions.run_python import run_python_file

__version__ = "0.0.3"

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Write or overwrite files
- Execute python files with optional list of arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

defined_functions: dict[str, Callable[..., str]] = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content,
    'write_file': write_file,
    'run_python_file': run_python_file
}

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

model_id = 'gemini-2.0-flash-001'

WORKING_DIRECTORY = os.path.abspath("./calculator")

def call_function(function_call: types.FunctionCall, verbose: bool = False) -> types.Content:
    function_name = function_call.name if function_call.name is not None else ""
    if function_name in defined_functions:
        kwargs = function_call.args if function_call.args is not None else {}
        kwargs['working_directory'] = WORKING_DIRECTORY

        if verbose:
            print(f'Calling function: {function_name}({kwargs})')
        else:
            print(f' - Calling function: {function_name}')

        result = defined_functions[function_name](**kwargs)
        return types.Content(
            role='tool',
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={'result': result},
                )
            ],
        )
    else:
        return types.Content(
            role='tool',
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f'Unknown function: {function_name}'}
                )
            ]
        )
    
def query_model(model: str, contents: list[types.Content], verbose: bool = False) -> types.GenerateContentResponse | None:
    response = None
    for _ in range(0, 20):
        response = client.models.generate_content(model=model_id, 
                                                      contents=contents, 
                                                      config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions]))
        
        candidates = response.candidates if response.candidates is not None else []
        for candidate in candidates:
            if candidate.content is not None:
                contents.append(candidate.content)

        if response.function_calls:
            for function_call in response.function_calls:
                result = call_function(function_call, verbose=verbose)
                contents.append(result)
                if result.parts is None or len(result.parts) < 1 or result.parts[0].function_response is None:
                    raise RuntimeError('Something went wrong')
                if verbose:
                    print('-> ', end='')
                    pprint(result.parts[0].function_response.response)
        else:
            break
    return response


if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(1)
    else:
        prompt = sys.argv[1]
        
        cla = []
        if len(sys.argv) > 2:
            cla = sys.argv[2:]

        verbose = True if '--verbose' in cla else False

        if '--version' in cla:
            print(f'{__version__}')
        else:    
            available_functions = types.Tool(
                function_declarations=DEFINED_SCHEMAS
            )

            client = genai.Client(api_key=api_key)

            messages: list[types.Content] = [
                types.Content(role='user', parts=[types.Part(text=prompt)])
            ]

            response = query_model(model_id, contents=messages, verbose=verbose)
            if response is None:
                print('Error')
            else:
                print(response.text)
                if verbose:
                    print(f'User prompt: {prompt}')
                    if response.usage_metadata is not None:
                        print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
                        print(f'Response tokens: {response.usage_metadata.candidates_token_count}')