import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def format_conversation(messages: list[dict]) -> str:
    """Convert stored messages into a readable transcript."""
    lines = []
    for msg in messages:
        role = "User" if msg["role"] == "user" else "Assistant"
        lines.append(f"{role}: {msg['content']}")
    return "\n".join(lines)


async def summarize_conversation(messages: list[dict]) -> str:
    """Send conversation to Groq and return a concise summary."""
    if not messages:
        return "No conversation to summarize yet."

    transcript = format_conversation(messages)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=512,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that summarizes WhatsApp conversations. "
                    "Provide a concise, clear summary in 3-5 bullet points. "
                    "Focus on key topics, decisions, and action items."
                ),
            },
            {
                "role": "user",
                "content": f"Please summarize this WhatsApp conversation:\n\n{transcript}",
            },
        ],
    )

    return response.choices[0].message.content


async def chat_with_groq(messages: list[dict]) -> str:
    """Send full conversation history to Groq and get an AI reply."""
    chat_messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly and helpful AI assistant on WhatsApp. "
                "Keep your replies concise and conversational. "
                "Answer questions, help with tasks, and engage naturally."
            ),
        }
    ]
    # Append the full conversation history for context
    chat_messages.extend(messages)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=512,
        messages=chat_messages,
    )

    return response.choices[0].message.content
