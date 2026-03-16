from unittest.mock import patch, MagicMock
from service.notion import create_invoice


def test_create_invoice():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "abc123", "object": "page"}

    with patch("service.notion.requests.post", return_value=mock_response) as mock_post:
        result = create_invoice(
            invoice_number="INV-001",
            client_name="Jane Smith",
            amount=5000.00,
            due_date="2026-04-01",
            description="Kitchen remodel deposit"
        )

        assert result["id"] == "abc123"

        payload = mock_post.call_args[1]["json"]
        assert payload["properties"]["Amount"]["number"] == 5000.00
        assert payload["properties"]["Status"]["select"]["name"] == "Unpaid"
        assert payload["properties"]["Invoice #"]["title"][0]["text"]["content"] == "INV-001"
        assert payload["properties"]["Client Name"]["rich_text"][0]["text"]["content"] == "Jane Smith"


def test_create_invoice_no_amount():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "abc123", "object": "page"}

    with patch("service.notion.requests.post", return_value=mock_response) as mock_post:
        result = create_invoice(
            invoice_number="INV-002",
            client_name="Jane Smith",
            amount=None,
            due_date="2026-04-01",
            description="Kitchen remodel deposit"
        )

        payload = mock_post.call_args[1]["json"]
        assert "Amount" not in payload["properties"]


def test_create_invoice_no_due_date():
    mock_response = MagicMock()
    mock_response.json.return_value = {"id": "abc123", "object": "page"}

    with patch("service.notion.requests.post", return_value=mock_response) as mock_post:
        result = create_invoice(
            invoice_number="INV-003",
            client_name="Jane Smith",
            amount=5000.00,
            due_date=None,
            description="Kitchen remodel deposit"
        )

        payload = mock_post.call_args[1]["json"]
        assert "Due Date" not in payload["properties"]
