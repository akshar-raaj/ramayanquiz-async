"""
Interacts with OpenAI to perform different things.
"""

from openai import OpenAI

def openai_result(content: str):
    """
    """
    client = OpenAI()
    try:
        completion = client.chat.completions.create(
            model='gpt-4.1-nano',
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"{content}"
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
