import os
from dotenv import load_dotenv
import openai

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_openai(prompt: str) -> str:
    try:
        client = openai.OpenAI()
        response = client.responses.create(
            model="gpt-5-nano",
            input=prompt,
            store=True
        )
        return response.output_text
    except Exception as e:
        return f"Erro ao chamar OpenAI: {e}"
