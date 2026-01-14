import os
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from config import (
    SHEETS_SCOPES,
    TOKEN_FILE,
    SPREADSHEET_ID,
    SHEET_NAME
)


def get_sheets_service():
    """
    Google Sheets API service return karta hai
    """
    creds = Credentials.from_authorized_user_file(
        TOKEN_FILE, SHEETS_SCOPES
    )
    service = build("sheets", "v4", credentials=creds)
    return service


def _get_existing_message_keys(service):
    """
    Sheet se existing rows read karta hai
    Duplicate prevent karne ke liye
    """
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A2:C"
    ).execute()

    rows = result.get("values", [])
    existing_keys = set()

    for row in rows:
        if len(row) >= 3:
            key = f"{row[0]}|{row[1]}|{row[2]}"
            existing_keys.add(key)

    return existing_keys


def append_emails_to_sheet(service, email_data_list):
    """
    Clean email data ko Google Sheet me append karta hai
    (Duplicate skip karke)
    """
    if not email_data_list:
        return

    existing_keys = _get_existing_message_keys(service)
    new_rows = []

    for email in email_data_list:
        key = f"{email['from']}|{email['subject']}|{email['date']}"
        if key in existing_keys:
            continue

        new_rows.append([
            email["from"],
            email["subject"],
            email["date"],
            email["content"]
        ])

    if not new_rows:
        return

    body = {
        "values": new_rows
    }

    service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID,
        range=f"{SHEET_NAME}!A:D",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body=body
    ).execute()
