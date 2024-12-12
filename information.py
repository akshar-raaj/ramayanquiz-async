"""
Interacts with OpenAI to retrieve some information/context for a particular question.
"""

from openai import OpenAI
from constants import CHATGPT_MODEL


def information(question: str):
    print(f"Retreiving information for {question}")
    client = OpenAI()
    try:
        completion = client.chat.completions.create(
            model=CHATGPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Provide me a concise information/context, or additional engaging information, for this particular Ramayana question. It shouldn't be more than 30 words."
                }
            ]
        )
    except Exception:
        print("Error in making request to OpenAI")
        return
    try:
        content = completion.choices[0].message.content
        return content
    except Exception:
        print("Error in parsing OpenAI result")
        return
    print(f"Retrieved information for {question}")
