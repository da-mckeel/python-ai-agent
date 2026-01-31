import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

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
response = client.models.generate_content(model='gemini-2.5-flash', contents=messages)
if response.usage_metadata == None:
    raise RuntimeError("Failed API Request")
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count


def main():
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print(f"Response: ")
        print(response.text)
    else:
        print(f"Response: ")
        print(response.text)

if __name__ == "__main__":
    main()
