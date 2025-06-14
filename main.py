import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

__version__ = "0.0.2"

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

model_id = 'gemini-2.0-flash-001'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit(1)
    else:
        prompt = sys.argv[1]
        
        cla = []
        if len(sys.argv) > 2:
            cla = sys.argv[2:]

        if '--version' in cla:
            print(f'{__version__}')
        else:    
            client = genai.Client(api_key=api_key)

            messages = [
                types.Content(role='user', parts=[types.Part(text=prompt)])
            ]

            response = client.models.generate_content(model=model_id, contents=messages)
            print(response.text)
            if '--verbose' in cla:
                print(f'User prompt: {prompt}')
                print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
                print(f'Response tokens: {response.usage_metadata.candidates_token_count}')