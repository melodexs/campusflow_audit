import json
import os

import requests

API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
DB_FILE = "ticket.json"

CATEGORIES = ["facilities", "it", "academic", "finance", "safety", "other"]
PRIORITIES = ["low", "medium", "high"]


def analyze_ticket(title, description):
    """Ask the model to triage a ticket. Returns a dict or None on failure."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("OPENROUTER_API_KEY is not set.")
        return None

    prompt = (
        "You triage campus support tickets. Reply with ONLY a JSON object with keys "
        f'"category" (one of {CATEGORIES}), "priority" (one of {PRIORITIES}) '
        'and "summary" (max 15 words).\n\n'
        f"Title: {title}\nDescription: {description}"
    )

    try:
        resp = requests.post(
            API_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            },
            timeout=30,
        )
        resp.raise_for_status()
        content = resp.json()["choices"][0]["message"]["content"].strip()

        # Some models wrap JSON in ```json fences; strip them.
        if content.startswith("```"):
            content = content.strip("`")
            if content.lower().startswith("json"):
                content = content[4:]
        data = json.loads(content.strip())

        category = str(data.get("category", "other")).lower()
        priority = str(data.get("priority", "medium")).lower()
        return {
            "category": category if category in CATEGORIES else "other",
            "priority": priority if priority in PRIORITIES else "medium",
            "summary": str(data.get("summary", "")).strip(),
        }
    except (requests.RequestException, KeyError, IndexError, ValueError) as e:
        print(f"AI request failed: {e}")
        return None


def main():
    print("_campusflow AI triage_")

    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        print("No tickets found. Create one with main.py first.")
        return

    with open(DB_FILE) as f:
        tickets = json.load(f)

    for t in tickets:
        print(f"#{t['id']} [{t['status']}] {t['title']}")

    try:
        choice = int(input("\nTicket id to analyze: "))
    except ValueError:
        print("Please enter a number.")
        return

    ticket = next((t for t in tickets if t["id"] == choice), None)
    if ticket is None:
        print(f"Ticket #{choice} not found.")
        return

    print("Analyzing with AI...")
    result = analyze_ticket(ticket["title"], ticket["description"])
    if result:
        print(f"\nCategory: {result['category']}")
        print(f"Priority: {result['priority']}")
        print(f"Summary:  {result['summary']}")


if __name__ == "__main__":
    main()