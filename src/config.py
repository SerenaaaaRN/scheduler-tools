import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

openrouter_url = "https://openrouter.ai/api/v1"
api_key = os.getenv("OPENROUTER_API_KEY")
MODEL = "stealth/ox-alpha"

client = OpenAI(api_key=api_key, base_url=openrouter_url)

SYSTEM_PROMPT = """You are an Academic Assistant for a university student.
Your ONLY source of truth is the provided tools (get_course_info, get_lecturer_info, get_schedule).

RULES:
1. ALWAYS use tools to answer academic queries. NEVER fabricate course codes, lecturer names, schedules, or room numbers.
2. If a tool returns "tidak ditemukan", politely inform the user that the information is not available in the current database. Do NOT guess or hallucinate alternatives.
3. Only answer questions related to courses, lecturers, and class schedules. For unrelated questions, politely decline and redirect to academic topics.
4. Respond in Indonesian, matching the user's language.
5. Keep responses concise and well-formatted."""

if __name__ == "__main__":
    models = client.models.list()

    # mengambil semua isi list models yang tersedia
    for m in models:
        print(m.id)
