import os
from dotenv import load_dotenv
import argparse
import json
from prompts import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()
# Now we can access `args.user_prompt`

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


agent_finished = False
limit = 20
for _ in range(limit):
    response = client.chat.completions.create(
    model="openrouter/free",
    messages=messages,
    tools=available_functions, 
    )
    message = response.choices[0].message
    messages.append(message)
    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)
            messages.append(result_message)
            if not result_message["content"]:
                raise Exception("No content returned")
            if args.verbose is True:
                print(f"-> {result_message['content']}")
    else:
        print(message.content)
        agent_finished = True
        break

if agent_finished is not True:
    print("Model has reached the maximum number of iterations and also has failed to reach a response")
 

if args.verbose is True:
    print(f"User prompt: {args.user_prompt}")
    print(f"Prompt tokens: {response.usage.prompt_tokens}")
    print(f"Response tokens: {response.usage.completion_tokens}") 

    exit(1)   