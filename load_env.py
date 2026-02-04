import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent / ".env"

# print(' ªªªªªªª env_path: ', env_path)

if not env_path.exists():
    raise FileNotFoundError(f"Env file not found at {env_path}")

load_dotenv(dotenv_path=env_path)

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    client = OpenAI(api_key=api_key)
    return client

# print('==========', get_openai_client())
