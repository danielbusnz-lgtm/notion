import os
import json
from dotenv import load_dotenv
from service.ms_graph import get_access_token, MS_GRAPH_BASE_URL
from service.microsoft_email import get_attachments
from service.email_parser import parse_email
from service.notion import create_invoice
import httpx

PROCESSED_EMAILS_FILE = "processed_emails.json"


def load_processed_emails():
    if os.path.exists(PROCESSED_EMAILS_FILE):
        with open(PROCESSED_EMAILS_FILE, "r") as f:
            return json.load(f)
    return []

def save_processed_emails(processed):
    with open(PROCESSED_EMAILS_FILE, "w") as f:
        json.dump(processed, f)

def handle_email(email,headers,processed):
    email_id = email["id"]

    if email_id in processed:
        return 

    subject = email.get("subject")
    sender = email["from"]["emailAddress"]["address"]
    body = email.get("body", {}).get("content", "")
    received_date = email.get("receivedDateTime", "")

    attachments = get_attachments(email_id, headers)
    parsed = parse_email(subject, sender, body, received_date, attachments)

    category = parsed.get("category")

    if category == "invoice":
        create_invoice(
            invoice_number=parsed.get("invoice_number", f"INV-{email_id[:8]}"),
            client_name=parsed.get("client_name", sender),
            amount=parsed.get("amount"),
            due_date=parsed.get("due_date"),
            description=parsed.get("description", subject)
        )
        print(f"Created invoice for {sender}")
    else:
        print(f"Skipping email from {sender} — category: {category}")

    processed.append(email_id)


def main():
    load_dotenv()
    APPLICATION_ID = os.getenv("APPLICATION_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    SCOPES = ["User.Read", "Mail.ReadWrite"]

    access_token = get_access_token(APPLICATION_ID, CLIENT_SECRET, SCOPES)

    headers = {"Authorization": "Bearer " + access_token}
    endpoint = f"{MS_GRAPH_BASE_URL}/me/messages"
    params = {"$top": 50, "$orderby": "receivedDateTime desc"}
    response = httpx.get(endpoint, headers=headers, params=params, timeout=10.0)
    emails = response.json().get("value", [])

    processed = load_processed_emails()

    for email in emails:
        handle_email(email, headers, processed)

    save_processed_emails(processed)


if __name__ == "__main__":
    main()
