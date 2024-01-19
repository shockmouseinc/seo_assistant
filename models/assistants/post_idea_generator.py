from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=api_key
)
def get_post_ideas(user_prompt, language, tone):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": "You are a blog post idea generator that takes an idea and returns three blog post ideas each with a title, and a brief paragraph outlining the subject of the post."},
            {"role": "user", "content": f"Write three blog post ideas for the following topic: {user_prompt}, in the following language: {language}, with the following writing tone: {tone}"}
        ]
    )

    return response.choices[0].message.content