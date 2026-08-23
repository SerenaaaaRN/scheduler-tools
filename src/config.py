import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

openrouter_url = "https://openrouter.ai/api/v1"
api_key = os.getenv("OPENROUTER_API_KEY")
MODEL = "stealth/ox-alpha"

client = OpenAI(api_key=api_key, base_url=openrouter_url)

if __name__ == "__main__":
    models = client.models.list()

    # mengambil semua isi list models yang tersedia
    for m in models:
        print(m.id)
