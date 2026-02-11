import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Missing Gemini API Key")

client = genai.Client(api_key=api_key)

# Prompting
parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

# Response
response = client.models.generate_content(
    model='gemini-2.5-flash', 
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0)
)
if response.usage_metadata == None:
    raise RuntimeError("Failed API Request")
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

def main():
    function_call_result = []

    for part in response.candidates[0].content.parts:
        if part.function_call:
            result = call_function(part.function_call, args.verbose)
            if not result.parts:
                raise Exception("No Parts")
            if result.parts[0].function_response == None:
                raise Exception("No FunctionResponse object")
            if result.parts[0].function_response.response == None:
                raise Exception("No Response Field")
            function_call_result.append(result.parts[0])
            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")

    if len(function_call_result) == 0:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")
        print("Response: ")
        print(response.text)

if __name__ == "__main__":
    main()
