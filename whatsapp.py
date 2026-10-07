import os
import httpx
from dotenv import load_dotenv

load_dotenv()

PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")
API_URL = f"https://graph.facebook.com/v19.0/{PHONE_NUMBER_ID}/messages"


async def send_whatsapp_message(to: str, text: str) -> dict:
    """Send a text message to a WhatsApp number via Meta Cloud API."""
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "type": "text",
        "text": {"body": text},
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        print(f"✅ Message sent to {to}")
        return response.json()
