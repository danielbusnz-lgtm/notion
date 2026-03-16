# Notion Business Organizer

Automatically reads emails from Microsoft Outlook and organizes them into Notion databases for a construction and home remodeling business.

## Overview

This tool fetches emails via the Microsoft Graph API, uses Claude AI to parse and categorize them, and creates records in Notion for invoices and shipment tracking.

## Features

- Fetches emails and attachments from Microsoft Outlook
- Parses emails using Claude AI (supports PDFs and images)
- Creates invoice records in Notion automatically
- Designed to run on a schedule

## Project Structure

```
notion/
├── service/
│   ├── ms_graph.py          # Microsoft OAuth token handling
│   ├── microsoft_email.py   # Fetches emails and attachments from Outlook
│   ├── notion.py            # Notion database operations
│   └── email_parser.py      # Claude AI email parsing
├── tests/
│   └── test_notion.py       # Unit tests
├── main.py                  # Main pipeline orchestrator
└── .env                     # Environment variables (not committed)
```

## Requirements

- Python 3.12+
- Microsoft Azure app with Mail.ReadWrite permissions
- Notion API key
- Anthropic API key

## Setup

1. Clone the repository
2. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and fill in your credentials:

```
ANTHROPIC_API_KEY=
NOTION_API_KEY=
INVOICES_DATABASE_ID=
APPLICATION_ID=
CLIENT_SECRET=
```

## Running Tests

```bash
pytest tests/
```

## Environment Variables

| Variable | Description |
|---|---|
| `ANTHROPIC_API_KEY` | Anthropic API key for Claude AI |
| `NOTION_API_KEY` | Notion integration token |
| `INVOICES_DATABASE_ID` | Notion database ID for invoices |
| `APPLICATION_ID` | Microsoft Azure application ID |
| `CLIENT_SECRET` | Microsoft Azure client secret |
