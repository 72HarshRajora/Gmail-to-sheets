import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from gmail_service import (
    get_gmail_service,
    fetch_unread_emails,
    get_email_payload
)

from email_parser import extract_email_data
from sheets_service import (
    get_sheets_service,
    append_emails_to_sheet
)

from config import (
    STATE_FILE,
    MARK_AS_READ_AFTER_PROCESS
)


def load_state():
    if not os.path.exists(STATE_FILE):
        return set()

    with open(STATE_FILE, "r") as f:
        data = json.load(f)
        return set(data.get("processed_ids", []))


def save_state(processed_ids):
    with open(STATE_FILE, "w") as f:
        json.dump(
            {"processed_ids": list(processed_ids)},
            f,
            indent=2
        )


def mark_email_as_read(service, message_id):
    service.users().messages().modify(
        userId="me",
        id=message_id,
        body={"removeLabelIds": ["UNREAD"]}
    ).execute()


def main():
    gmail_service = get_gmail_service()
    sheets_service = get_sheets_service()

    processed_ids = load_state()
    unread_messages = fetch_unread_emails(gmail_service)

    email_rows = []
    new_processed_ids = set(processed_ids)

    for msg in unread_messages:
        msg_id = msg["id"]

        if msg_id in processed_ids:
            continue

        full_message = get_email_payload(gmail_service, msg_id)
        email_data = extract_email_data(full_message)

        if not email_data:
            new_processed_ids.add(msg_id)
            continue

        email_rows.append(email_data)
        new_processed_ids.add(msg_id)

        if MARK_AS_READ_AFTER_PROCESS:
            mark_email_as_read(gmail_service, msg_id)

    append_emails_to_sheet(sheets_service, email_rows)
    save_state(new_processed_ids)


if __name__ == "__main__":
    main()
