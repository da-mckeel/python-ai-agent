import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if api_key == None:
    raise RuntimeError("Missing Gemini API Key")

client = genai.Client(api_key=api_key)
prompt = 'Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.'
response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)
if response.usage_metadata == None:
    raise RuntimeError("Failed API Request")
prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count


def main():
    print(f"User prompt: {prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
    print(f"Response: ")
    print(response.text)

if __name__ == "__main__":
    main()
