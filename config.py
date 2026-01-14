import os

# -----------------------------
# Google API Scopes
# -----------------------------
GMAIL_SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]

SHEETS_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets"
]

# -----------------------------
# Credentials & Token Paths
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CREDENTIALS_FILE = os.path.join(
    BASE_DIR, "credentials", "credentials.json"
)

TOKEN_FILE = os.path.join(
    BASE_DIR, "credentials", "token.json"
)

# -----------------------------
# Google Sheet Configuration
# -----------------------------
# NOTE: Spreadsheet ID baad me set hoga
SPREADSHEET_ID = "1TVzkIlkj1xpcerO8mJ_ZA_CyoI4bw-rSO6wpuWkQnco"   # <-- later fill karenge
SHEET_NAME = "Sheet1"

# -----------------------------
# State Persistence
# -----------------------------
# Last processed email ka history store karne ke liye
STATE_FILE = os.path.join(
    BASE_DIR, "credentials", "state.json"
)

# -----------------------------
# Email Processing Rules
# -----------------------------
PROCESS_ONLY_UNREAD = True
MARK_AS_READ_AFTER_PROCESS = True

# Bonus filters
EXCLUDE_NO_REPLY = True
NO_REPLY_KEYWORDS = ["no-reply", "noreply", "do-not-reply"]

SUBJECT_KEYWORD_FILTER = None
# Example:
# SUBJECT_KEYWORD_FILTER = "Invoice"

# -----------------------------
# Retry Configuration (Bonus)
# -----------------------------
MAX_RETRY_ATTEMPTS = 3
RETRY_WAIT_SECONDS = 2
