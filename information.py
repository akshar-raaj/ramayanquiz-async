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
                    "content": f"Provide me a concise and engaging information for this question. If possible, provide me info on the most important noun in this question. It shouldn't be more than 30 words. The question is: {question}"
                }
            ]
        )
    except Exception:
        print("Error in making request to OpenAI")
        return
    try:
        content = completion.choices[0].message.content
        print(f"Retrieved information for {question}")
        return content
    except Exception:
        print("Error in parsing OpenAI result")
        return
