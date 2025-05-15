"""
Interacts with OpenAI to translate the provided English text to another language.

Currently tested with the following:
- Hindi
- Telugu
"""

from openai import OpenAI
from constants import CHATGPT_MODEL

from cache import get_connection as get_redis_connection


def read_cache(english_text, target_language):
    redis_connection = get_redis_connection()
    key = f"translation-{target_language}-{english_text}"
    bytes_value = redis_connection.get(key)
    if bytes_value is None:
        return bytes_value
    value = bytes_value.decode('utf-8')
    return value


def write_cache(english_text, target_language, translation):
    bytes_translation = translation.encode('utf-8')
    redis_connection = get_redis_connection()
    key = f"translation-{target_language}-{english_text}"
    redis_connection.set(key, bytes_translation)


def translate(english_text: str, translate_to: str = 'Hindi'):
    """
    This refers the cache first.
    If the value is available in cache, then no OpenAI invocation happens.
    This allows keeping the cost in check.
    """
    value = read_cache(english_text, translate_to)
    if value is not None:
        print(f"Translation for {english_text} to {translate_to} available in cache.")
        return value
    print(f"Translating {english_text} to {translate_to}")
    client = OpenAI()
    try:
        completion = client.chat.completions.create(
            model=CHATGPT_MODEL,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": f"Translate the following text to {translate_to}: {english_text}"
                }
            ]
        )
    except Exception:
        print("Error in making request to OpenAI")
        return
    try:
        content = completion.choices[0].message.content
        print(f"Translated {english_text} to {translate_to}")
        write_cache(english_text, translate_to, content)
        return content
    except Exception:
        print("Error in parsing OpenAI result")
        return
