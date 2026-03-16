import os
import json
import anthropic

client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env

def parse_email(subject, sender, body, received_date, attachments=None):
    prompt = f"""You are an assistant for a construction and home remodeling business.

Analyze this email and extract key information.

Subject: {subject}
From: {sender}
Date: {received_date}
Body:
{body}

Return ONLY a JSON object with these fields:
- category: "lead", "project_update", "invoice", or "other"
- client_name
- client_email
- address
- job_type
- description
- amount
- priority: "high", "medium", or "low"
"""

    if attachments:
        content = [{"type": "text", "text": prompt}]
        for a in attachments:
            if "image" in a["content_type"]:
                content.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": a["content_type"],
                        "data": a["content_bytes"]
                    }
                })
            elif a["content_type"] == "application/pdf":
                content.append({
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": a["content_bytes"]
                    }
                })
    else:
        content = prompt

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[{"role": "user", "content": content}]
    )

    text = next((b.text for b in response.content if b.type == "text"), "{}")

    return json.loads(text)
