from UI4AI import run_chat
import openai

openai.api_key = "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"

def generate_response(messages) -> str:
    """Generate response with history management"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Response generation failed: {str(e)}")

run_chat(
    generate_response=generate_response,
    page_title="GPT-4 Chat",
    chat_placeholder="Ask me anything...",
    sidebar_instructions="Powered by GPT-4",
    spinner_text="Generating response...",
)