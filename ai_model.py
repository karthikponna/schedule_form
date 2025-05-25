# ai_model.py

import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = (
    "You are a JSON-only classifier.  The user gives one paragraph describing their business "
    "and how big they are.  Reply with exactly one object and no extra keys/text:\n"
    '{"status":"qualified"}     – real business + mentions scale\n'
    '{"status":"not qualified"} – admits no business or just testing\n'
    '{"status":"more info"}     – mentions business but no scale\n\n'
    "Example:\n"
    "User: \"FreshBites serves 200 clients weekly with $1M ARR.\"\n"
    "Assistant: {\"status\":\"qualified\"}\n\n"
    "Now classify the next user input and return only the JSON."
)

def classify_business(text: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user",  "content":text}
        ],
        
        max_completion_tokens=30,
    )
    raw = resp.choices[0].message.content or ""
    print("🔍 Raw model output:", repr(raw))

    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        print("⚠️ JSON decode error on:", repr(raw))
        return {"status":"more info"}
