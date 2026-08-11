import os

from dotenv import load_dotenv

load_dotenv()


def _split_csv(value: str) -> list:
    return [v.strip() for v in value.split(",") if v.strip()]


class Config:
    # ------------------------------------------------------------------
    # General
    # ------------------------------------------------------------------
    STORAGE_BACKEND = os.environ.get("STORAGE_BACKEND", "mysql").lower()  # "mysql" | "google_sheets"
    ALLOWED_ORIGINS = _split_csv(
        os.environ.get(
            "ALLOWED_ORIGINS",
            "http://localhost:8000,http://127.0.0.1:8000",
        )
    )
    ADMIN_API_KEY = os.environ.get("ADMIN_API_KEY", "")

    # ------------------------------------------------------------------
    # MySQL
    # ------------------------------------------------------------------
    MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))
    MYSQL_USER = os.environ.get("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "")
    MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE", "gotech_contact")

    # ------------------------------------------------------------------
    # Google Sheets
    # ------------------------------------------------------------------
    GOOGLE_SERVICE_ACCOUNT_FILE = os.environ.get(
        "GOOGLE_SERVICE_ACCOUNT_FILE", "service-account.json"
    )
    GOOGLE_SHEET_ID = os.environ.get("GOOGLE_SHEET_ID", "")
    GOOGLE_SHEET_WORKSHEET = os.environ.get("GOOGLE_SHEET_WORKSHEET", "Submissions")
