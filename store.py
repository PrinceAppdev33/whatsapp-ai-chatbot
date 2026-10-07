"""
Simple in-memory conversation store.
Replace with Redis or a database for production use.
"""

from collections import defaultdict

# { phone_number: [ {role, content}, ... ] }
_conversations: dict[str, list[dict]] = defaultdict(list)


def add_message(phone: str, role: str, content: str) -> None:
    """Append a message to a user's conversation history."""
    _conversations[phone].append({"role": role, "content": content})


def get_conversation(phone: str) -> list[dict]:
    """Return the full conversation history for a user."""
    return _conversations[phone]


def clear_conversation(phone: str) -> None:
    """Clear a user's conversation history."""
    _conversations[phone] = []
