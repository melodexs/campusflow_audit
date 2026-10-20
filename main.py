import json
import os

DB_FILE = "ticket.json"

print ("_campusflow_")
title = input("Enter ticket title")
desc = input("Enter ticket description")

ticket = json.load(open(DB_FILE)) if os.path.exists(DB_FILE) and os.path.getsize(DB_FILE) > 0 else []

tk_id = ticket[-1]["id"] + 1 if ticket else 1
ticket.append({"id": tk_id, "title": title, "description": desc, "status": "open"})

with open(DB_FILE, "w") as f:
    json.dump(ticket, f, indent=4)
print (f" ticket #{tk_id} created successfully!")