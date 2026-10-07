# WhatsApp → LLM Summarization Pipeline

Real-time WhatsApp message ingestion via Meta Cloud API, with Claude summarization.

## Project Structure

```
whatsapp_pipeline/
├── main.py          # FastAPI webhook server
├── llm.py           # Claude summarization logic
├── whatsapp.py      # Send messages via Meta API
├── store.py         # In-memory conversation store
├── .env.example     # Environment variable template
└── requirements.txt
```

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure environment
```bash
cp .env.example .env
# Fill in your keys in .env
```

### 3. Run the server
```bash
uvicorn main:app --reload --port 3000
```

### 4. Expose locally with ngrok
```bash
ngrok http 3000
# Copy the https URL e.g. https://abc123.ngrok.io
```

### 5. Register Webhook in Meta Dashboard
- Go to your app → WhatsApp → Configuration
- Webhook URL: `https://abc123.ngrok.io/webhook`
- Verify Token: same value as `WHATSAPP_VERIFY_TOKEN` in your `.env`
- Subscribe to: `messages`

## How It Works

1. User sends a WhatsApp message to your test number
2. Meta forwards it to your `/webhook` endpoint
3. The message is stored in conversation history
4. Every 5 messages **or** if the user sends "summarize", Claude summarizes the conversation
5. The summary is sent back to the user via WhatsApp

## Scaling to Production

- Replace `store.py` with **Redis** or **PostgreSQL** for persistent storage
- Use a **permanent access token** (via Meta System Users)
- Deploy to **Railway, Render, or AWS** instead of ngrok
