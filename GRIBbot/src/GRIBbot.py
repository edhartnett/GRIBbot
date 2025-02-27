import os
from dotenv import load_dotenv, find_dotenv

class GRIBbot:
    def __init__(self):
        print("GRIBbot initialized")

    def main(self):
        print("GRIBbot main")

if __name__=="__main__":
    gribbot = GRIBbot()
    gribbot.main()
    
load_dotenv(find_dotenv())
print(os.getenv("OPENAI_API_KEY"))

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Say this is a test",
        }
    ],
    model="gpt-3.5-turbo",
)