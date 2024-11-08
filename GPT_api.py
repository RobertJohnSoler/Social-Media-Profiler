from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(
    api_key = api_key,
    organization='org-wmGdyLBBqM7dSJjN05loCRgy',
    project='proj_bBXhXrZtZ0MrTuGqD545CCf0',
)

system_prompt = ''

with open("system_prompt.txt", "r") as file:
    system_prompt = file.read()

def sendTweetsToGPT(tweets):
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": str(tweets)}
    ]
    )
    return completion.choices[0].message.content