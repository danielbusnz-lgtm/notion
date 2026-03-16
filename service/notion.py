import requests
import os
import json
from datetime import datetime, timezone

NOTION_TOKEN = os.environ["NOTION_API_KEY"]

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)
    return response.json().get("results", [])

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    payload = {"properties": data}
    res = requests.patch(url, json=payload, headers=headers)
    return res

def create_invoice(invoice_number, client_name, amount, due_date, description):
    url = "https://api.notion.com/v1/pages"
    properties = {
        "Invoice #": {"title": [{"text": {"content": invoice_number}}]},
        "Client Name": {"rich_text": [{"text": {"content": client_name}}]},
        "Description": {"rich_text": [{"text": {"content": description}}]},
        "Status": {"select": {"name": "Unpaid"}},
    }
    if amount is not None:
        properties["Amount"] = {"number": amount}
    if due_date is not None:
        properties["Due Date"] = {"date": {"start": due_date}}

    payload = {
        "parent": {"database_id": os.environ["INVOICES_DATABASE_ID"]},
        "properties": properties
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# TODO: add create_shipment()
