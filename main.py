import json
import os

from ai_helper import analyze_ticket

DB_FILE = "ticket.json"


def load_tickets():
    if not os.path.exists(DB_FILE) or os.path.getsize(DB_FILE) == 0:
        return []

    with open(DB_FILE, "r", encoding="utf-8") as file:
        tickets = json.load(file)

    if not isinstance(tickets, list):
        raise ValueError("ticket.json must contain a JSON list")

    return tickets


def save_tickets(tickets):
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def create_ticket():
    print("\n_campusflow_")
    print("Create a new ticket")

    title = input("Enter ticket title: ").strip()
    description = input("Enter ticket description: ").strip()

    if not title or not description:
        print("Title and description cannot be empty.")
        return

    tickets = load_tickets()

    ticket_id = max(
        (ticket.get("id", 0) for ticket in tickets),
        default=0,
    ) + 1

    ticket = {
        "id": ticket_id,
        "title": title,
        "description": description,
        "status": "open",
    }

    print("\nAnalyzing ticket with AI...")

    try:
        ai_result = analyze_ticket(title, description)

        ticket["ai_analysis"] = ai_result

        print("\nAI analysis completed successfully!")

        print(f"Category: {ai_result['category']}")
        print(f"Priority: {ai_result['priority']}")
        print(f"Summary: {ai_result['ai_summary']}")
        print(f"Suggested solution: {ai_result['suggested_solution']}")

    except Exception as error:
        print(f"\nAI analysis failed: {error}")
        print("The ticket will still be saved without AI analysis.")

    tickets.append(ticket)

    save_tickets(tickets)

    print(f"\nTicket #{ticket_id} created successfully!")


if __name__ == "__main__":
    create_ticket()