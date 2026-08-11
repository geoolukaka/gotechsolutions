import datetime
import threading

import gspread
from google.oauth2.service_account import Credentials

from .base import SubmissionStorage

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
]

HEADER_ROW = [
    "Timestamp",
    "Name",
    "Email",
    "Phone",
    "Service",
    "Message",
    "Page URL",
    "IP Address",
]


class GoogleSheetsStorage(SubmissionStorage):
    """Stores each submission as a new row in a Google Sheet, using a
    service account (no manual OAuth flow, no Apps Script web app needed).

    Setup:
      1. Create a Google Cloud project, enable the Google Sheets API.
      2. Create a service account, download its JSON key, save it as
         `service-account.json` next to this backend (or point
         GOOGLE_SERVICE_ACCOUNT_FILE at it).
      3. Share your Google Sheet with the service account's email address
         (found in the JSON key as `client_email`), with Editor access.
      4. Put the sheet's ID (from its URL) in GOOGLE_SHEET_ID in .env.
    """

    def __init__(self, service_account_file: str, sheet_id: str, worksheet_name: str):
        if not sheet_id:
            raise ValueError("GOOGLE_SHEET_ID is not set in the environment.")

        self._lock = threading.Lock()
        creds = Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
        client = gspread.authorize(creds)
        spreadsheet = client.open_by_key(sheet_id)

        try:
            self._worksheet = spreadsheet.worksheet(worksheet_name)
        except gspread.WorksheetNotFound:
            self._worksheet = spreadsheet.add_worksheet(
                title=worksheet_name, rows=1000, cols=len(HEADER_ROW)
            )

        self._ensure_header()

    def _ensure_header(self):
        first_row = self._worksheet.row_values(1)
        if first_row != HEADER_ROW:
            self._worksheet.update("A1", [HEADER_ROW])
            self._worksheet.freeze(rows=1)

    def save_submission(self, data: dict) -> str:
        row = [
            datetime.datetime.utcnow().isoformat(),
            data["name"],
            data["email"],
            data.get("phone", ""),
            data.get("service", ""),
            data["message"],
            data.get("page", ""),
            data.get("ip_address", ""),
        ]
        # gspread's client isn't guaranteed thread-safe under concurrent
        # writes from Flask's threaded dev server, so serialize appends.
        with self._lock:
            self._worksheet.append_row(row, value_input_option="USER_ENTERED")
            row_count = len(self._worksheet.col_values(1))
        return str(row_count - 1)  # -1 to exclude the header row

    def list_submissions(self, limit: int = 50) -> list:
        records = self._worksheet.get_all_records()
        return records[-limit:][::-1]
