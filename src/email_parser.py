import base64
from bs4 import BeautifulSoup
from datetime import datetime
from email.utils import parsedate_to_datetime

from config import (
    EXCLUDE_NO_REPLY,
    NO_REPLY_KEYWORDS,
    SUBJECT_KEYWORD_FILTER
)


def _get_header(headers, name):
    for header in headers:
        if header["name"].lower() == name.lower():
            return header["value"]
    return ""


def _decode_body(body_data):
    if not body_data:
        return ""

    decoded_bytes = base64.urlsafe_b64decode(body_data)
    return decoded_bytes.decode("utf-8", errors="ignore")


def extract_email_data(message):
    """
    Gmail API message se clean email data nikalta hai
    """
    payload = message.get("payload", {})
    headers = payload.get("headers", [])

    sender = _get_header(headers, "From")
    subject = _get_header(headers, "Subject")
    date_raw = _get_header(headers, "Date")

    # Subject-based filtering (Bonus)
    if SUBJECT_KEYWORD_FILTER:
        if SUBJECT_KEYWORD_FILTER.lower() not in subject.lower():
            return None

    # No-reply filtering (Bonus)
    if EXCLUDE_NO_REPLY:
        sender_lower = sender.lower()
        for keyword in NO_REPLY_KEYWORDS:
            if keyword in sender_lower:
                return None

    # Date parsing
    try:
        date_obj = parsedate_to_datetime(date_raw)
        received_date = date_obj.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        received_date = date_raw

    # Body extraction
    body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            mime_type = part.get("mimeType", "")
            body_data = part.get("body", {}).get("data")

            if mime_type == "text/plain" and body_data:
                body = _decode_body(body_data)
                break

            elif mime_type == "text/html" and body_data and not body:
                html = _decode_body(body_data)
                soup = BeautifulSoup(html, "html.parser")
                body = soup.get_text(separator="\n")
    else:
        body_data = payload.get("body", {}).get("data")
        body = _decode_body(body_data)

    return {
        "from": sender,
        "subject": subject,
        "date": received_date,
        "content": body.strip()
    }
