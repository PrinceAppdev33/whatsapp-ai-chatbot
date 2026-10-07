"""Quick test to verify Groq + openai/gpt-4o-mini works."""
import asyncio
import sys
import os

# Add project dir to path
sys.path.insert(0, os.path.dirname(__file__))

from llm import summarize_conversation

sample_messages = [
    {"role": "user", "content": "Hey, are we meeting tomorrow at 10am?"},
    {"role": "assistant", "content": "Yes! Conference room B. Don't forget the slides."},
    {"role": "user", "content": "Got it. Should I bring the Q3 report too?"},
    {"role": "assistant", "content": "Yes please, the manager wants to review it."},
]

async def main():
    print("Testing Groq API with openai/gpt-4o-mini model...")
    try:
        result = await summarize_conversation(sample_messages)
        print("\n✅ SUCCESS! Summary:\n")
        print(result)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

asyncio.run(main())
