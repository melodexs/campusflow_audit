import os
import json
import requests

from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

MODEL = os.getenv("OPENROUTER_MODEL")


def analyze_ticket(title, description):
    if not API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY is missing from .env")

    if not MODEL:
        raise RuntimeError("OPENROUTER_MODEL is missing from .env")

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an assistant for a campus ticket management system. "
                    "Analyze the user's ticket and return valid JSON only, "
                    "with these fields: category, priority, ai_summary, "
                    "suggested_solution. "
                    "Use a short category such as Network, Hardware, Software, "
                    "Account, or Other. "
                    "Priority must be low, medium, or high. "
                    "Do not claim that you have fixed the problem."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Ticket title: {title}\n"
                    f"Ticket description: {description}"
                ),
            },
        ],
        "temperature": 0.2,
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    result = response.json()

    content = result["choices"][0]["message"]["content"]

    return json.loads(content)