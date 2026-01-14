# Gmail to Google Sheets Automation

## Author
Harsh Rajora

---

## 📖 Project Overview
This project is a Python-based automation system that reads real incoming **unread emails** from a Gmail account and logs them into a **Google Sheet** automatically.

The system uses:
- Gmail API
- Google Sheets API
- OAuth 2.0 (Desktop App)

Only **new unread emails** are processed, and duplicates are strictly avoided.

---

## 🎯 Objective
Each qualifying email is added as a new row in Google Sheets with the following fields:

| Column | Description |
|------|------------|
| From | Sender email address |
| Subject | Email subject |
| Date | Date & time received |
| Content | Email body (plain text) |

---

## 🏗️ High-Level Architecture (Text Diagram)

Gmail Inbox (Unread Emails)  
        |  
        v  
   Gmail API (OAuth 2.0)  
        |  
        v  
 Email Parser (clean data)  
        |  
        v  
 Duplicate Check + State  
        |  
        v  
 Google Sheets API  
        |  
        v  
 Google Sheet (Append Rows)  


---

## 🛠️ Tech Stack
- Python 3
- Gmail API
- Google Sheets API
- OAuth 2.0 (Desktop App)
- BeautifulSoup (HTML → Text)
- Tenacity (Retry Logic)

---

## 📂 Project Structure
Gmail-to-sheets/  
├── src/  
│ ├── gmail_service.py  
│ ├── sheets_service.py  
│ ├── email_parser.py  
│ └── main.py  
├── credentials/  
│ └── credentials.json (DO NOT COMMIT)  
├── proof/  
├── config.py  
├── requirements.txt  
├── .gitignore  
└── README.md  

---

## 🔐 OAuth Flow Used
- OAuth 2.0 Desktop Application flow
- User manually authorizes Gmail & Google Sheets access
- Token is stored locally (`token.json`) for reuse
- No service accounts are used

---

## 🔁 Duplicate Prevention Logic
Two-layer protection is used:
1. **State File (`state.json`)**
   - Stores processed Gmail message IDs
2. **Sheet-Level Check**
   - Composite key: `From + Subject + Date`

This ensures the same email is never inserted twice.

---

## 💾 State Persistence Method
- A local file `state.json` stores processed email IDs
- On re-run, previously processed emails are skipped
- Chosen because it is:
  - Simple
  - Reliable
  - Easy to explain & debug

---

## ⭐ Bonus Features Implemented
- Subject-based filtering (configurable)
- HTML email → plain text conversion
- No-reply email exclusion
- Retry logic for API failures
- Logging-ready modular structure

---

## 📸 Proof of Execution
The `/proof` folder contains:
- Gmail inbox screenshot (unread emails)
- Google Sheet populated with data
- OAuth consent screen screenshot
- Short screen-recorded demo video

---

## ⚠️ Security Rules Followed
- credentials.json is NOT committed
- OAuth tokens are NOT committed
- Sensitive files are ignored via `.gitignore`

---

## 🚧 Challenges Faced & Solution
**Challenge:** OAuth 403 errors due to insufficient scopes  
**Solution:**  
Combined Gmail and Google Sheets scopes into a single OAuth flow and regenerated the token after updating the consent screen.

---

## ⚠️ Limitations
- Processes only unread inbox emails
- Requires manual OAuth consent on first run
- Depends on Google API availability

---

## ▶️ How to Run the Project

```bash
python src/main.py
