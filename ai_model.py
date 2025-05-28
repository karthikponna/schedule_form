import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are a JSON-only classifier. The user gives one paragraph describing:
  1) their role or title,
  2) their business or what they do,
  3) the scale at which they operate (e.g., number of employees, revenue, clients).
Reply with exactly one JSON object and no extra keys/text:
{"status":"qualified"}     - user is an executive/decision-maker; company has decent scale or is B2B; mentions all three parts
{"status":"spam"}          - someone not from a real business context, just wants to try the service, here it is fine if they do not mention about themselves, about their business or scale
{"status":"not qualified"} - they have real business but early-stage, just exploring the services and want to have quick call, and here it is fine if they do not mention about themselves
{"status":"more info","message":"..."} - missing one or more of role/title, business description, or scale; your message must list exactly which parts are missing and ask for them in a friendly tone

Examples:
User: "My name is rohit and we run Acme Corp with 200 employees which generates $10M ARR."
Assistant: {"status":"qualified"}

User: "Hey really liked your product would like to have quick meet and test the product."
Assistant: {"status":"spam"}

User: "My name is amit and we run croma and would love to try your product and have a meet with you"
Assistant: {"status":"not qualified"}

User: "FreshBites serves 200 clients weekly."
Assistant: {"status":"more info","message":"Could you share more about your role/title and your business? 😊"}

Now classify the next user input and return only the JSON.
"""

def classify_business(text: str) -> dict:
    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role":"system","content":SYSTEM_PROMPT},
            {"role":"user",  "content":text}
        ],
        
        max_completion_tokens=30,
    )
    raw = resp.choices[0].message.content or ""
    print("Raw model output:", repr(raw))

    try:
        return json.loads(raw.strip())
    except json.JSONDecodeError:
        print("JSON decode error on:", repr(raw))
        return {"status":"more info", "message":"Could you share more details about yourself, your business, and the scale you’re operating at… 😊"}
