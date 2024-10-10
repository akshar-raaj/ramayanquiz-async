import os
from dotenv import load_dotenv

load_dotenv()


DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHATGPT_MODEL = 'gpt-4o'
