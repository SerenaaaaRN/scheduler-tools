import json
import gradio as gr
import logging
from config import client, MODEL, SYSTEM_PROMPT
from tools.handlers import execute_tool
from tools.registry import TOOLS_SCHEMA

logger = logging.getLogger(__name__)

def chat_with_tools(message: str, history: list = None) -> str:

    messages = (history or [{"role": "system", "content": SYSTEM_PROMPT}]).copy()
    messages.append({"role": "user", "content": message})

    try:
        for _ in range(5):
            response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=TOOLS_SCHEMA, tool_choice="auto", streaming=True
            )

            assistant_msg = response.choices[0].message

            if not assistant_msg.tool_calls:
                return assistant_msg.content or ""

            messages.append({
                "role": "assistant",
                "content": assistant_msg.content,
                "tool_calls": [tc.model_dump() for tc in assistant_msg.tool_calls]
            })

            for tc in assistant_msg.tool_calls:
                try:
                    args = json.loads(tc.function.arguments)
                except json.JSONDecodeError as e:
                    logger.warning("Gagal parse arguments tool %s: %s", tc.function.name, e)
                    args = {}

                result = execute_tool(tc.function.name, args)
                messages.append({
                    "role": "tool",
                    "content": result,
                    "tool_call_id": tc.id
                })
        
        fallback = client.chat.completions.create(model=MODEL, messages=messages, streaming=True)
        return fallback.choices[0].message.content or ""
    
    except Exception:
        logger.exception("Error dalam agents loop")
        return "Maaf, terjadi kesalahan saat memproses permintaan Anda."


with gr.Blocks(title="Scheluder Tools") as demo:
    gr.Markdown("Scheluder Tools")
    gr.Markdown("Ask me anything about your schedule!")

    chatbot = gr.ChatInterface(
        fn=chat_with_tools,
        examples=[
            "Siapa dosen yang mengajar Basis Data?",
            "Jadwal hari senin apa saja?",
            "Kapan kelas Kecerdasan Buatan?",
        ],
    )

if __name__ == "__main__":
    demo.launch()
