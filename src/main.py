import json
import gradio as gr
from config import client, MODEL
from tools.handlers import execute_tool
from tools.registry import TOOLS_SCHEMA


MAX_ITERATIONS = 5


def chat_with_tools(message: str, history: list = None) -> str:

    if history is None:
        messages = []
    else:
        messages = history.copy()

    messages.append({"role": "user", "content": message})

    try:
        for _ in range(MAX_ITERATIONS):
            response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=TOOLS_SCHEMA, tool_choice="auto"
            )

            assistant_message = response.choices[0].message

            if assistant_message.tool_calls:
                messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_message.content,
                        "tool_calls": assistant_message.tool_calls,
                    }
                )

                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    arguments = json.loads(tool_call.function.arguments)

                    result = execute_tool(tool_name, arguments)

                    messages.append(
                        {"role": "tool", "tool_call_id": tool_call.id, "content": result}
                    )
            else:
                return assistant_message.content or ""

        # Max iterations reached; force a natural response without tools
        final_response = client.chat.completions.create(model=MODEL, messages=messages)
        return final_response.choices[0].message.content or ""

    except Exception as e:
        return f"Error: {str(e)}"


def chatbot_response(message, history):
    messages = []

    if history:
        for item in history:
            if isinstance(item, dict):
                messages.append(item)
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                user_msg, bot_msg = item[0], item[1]
                if user_msg:
                    messages.append({"role": "user", "content": str(user_msg)})
                if bot_msg:
                    messages.append({"role": "assistant", "content": str(bot_msg)})

    response = chat_with_tools(message, messages)
    
    return response or "Maaf, saya tidak bisa memproses permintaan Anda."


with gr.Blocks(title="Academic Assistant") as demo:
    gr.Markdown("# Academic Assistant")
    gr.Markdown("Ask me anything about your academic tasks!")

    chatbot = gr.ChatInterface(
        fn=chatbot_response,
        examples=[
            "Apa detail mata kuliah Pemrograman Dasar?",
            "Siapa dosen yang mengajar Basis Data?",
            "Jadwal hari senin apa saja?",
            "Kapan kelas Kecerdasan Buatan?",
        ],
        title=None,
        description=None,
    )

if __name__ == "__main__":
    demo.launch()
