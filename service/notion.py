from types import resolve_bases
import requests
import os
import requests
from datetime import datetime, timezone

NOTION_TOKEN = os.environ["NOTION_API_KEY"] 
DATABASE_ID = "3149daa54a588051b989ce099b615b00"

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    payload = {"page_size":100}
    response = requests.post(url, json=payload, headers=headers)

    data =  response.json()

    import json
    with open('db.json', 'w', encoding= 'utf8') as f:
        json.dump(data,f,ensure_ascii=False, indent=4)

    results=data["results"]

    return results

pages = get_pages()
print(pages)

for page in pages:
    page_id = page["id"]
    print(page_id)
    props = page["properties"]
    created =page["created_time"] 
    print(created)
    url = page["url"]
    print(url)
    title = props["Title"]["rich_text"][0]["text"]["content"]
    published = props["Published"]["date"]["start"]
    published = datetime.fromisoformat(published)

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res


update_page("3149daa5-4a58-802b-b65b-f97255a5e0b6",)
