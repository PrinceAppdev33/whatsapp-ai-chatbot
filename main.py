import os
import httpx
from fastapi import FastAPI, Request, Query
from dotenv import load_dotenv
from llm import summarize_conversation, chat_with_groq
from whatsapp import send_whatsapp_message
from store import add_message, get_conversation

load_dotenv()

app = FastAPI()

VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN")


# ── Webhook verification (Meta calls this once during setup) ──────────────────
@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token"),
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        print("✅ Webhook verified by Meta")
        return int(hub_challenge)
    return {"error": "Verification failed"}, 403


# ── Incoming messages ─────────────────────────────────────────────────────────
@app.post("/webhook")
async def receive_message(request: Request):
    body = await request.json()

    try:
        entry = body["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        # Ignore status updates (delivered, read, etc.)
        if "messages" not in value:
            return {"status": "ignored"}

        message = value["messages"][0]
        sender = message["from"]          # sender's WhatsApp number
        msg_type = message.get("type")

        # Only handle text messages
        if msg_type != "text":
            return {"status": "non-text ignored"}

        text = message["text"]["body"]
        print(f"📩 Message from {sender}: {text}")

        # Store user message in conversation history
        add_message(sender, role="user", content=text)
        conversation = get_conversation(sender)

        # Special command: "summarize" → return a summary
        if text.strip().lower() == "summarize":
            reply = await summarize_conversation(conversation)
            reply = f"📝 *Summary:*\n{reply}"
        else:
            # Always reply to every message using Groq
            reply = await chat_with_groq(conversation)

        print(f"🤖 Reply to {sender}: {reply}")

        # Store assistant reply and send it
        add_message(sender, role="assistant", content=reply)
        await send_whatsapp_message(sender, reply)

    except (KeyError, IndexError) as e:
        print(f"⚠️  Unexpected payload structure: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

    return {"status": "ok"}
