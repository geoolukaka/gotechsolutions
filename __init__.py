from .base import SubmissionStorage
from .google_sheets_storage import GoogleSheetsStorage
from .mysql_storage import MySQLStorage


def get_storage_backend(config) -> SubmissionStorage:
    backend = config["STORAGE_BACKEND"]

    if backend == "google_sheets":
        return GoogleSheetsStorage(
            service_account_file=config["GOOGLE_SERVICE_ACCOUNT_FILE"],
            sheet_id=config["GOOGLE_SHEET_ID"],
            worksheet_name=config["GOOGLE_SHEET_WORKSHEET"],
        )

    if backend == "mysql":
        return MySQLStorage(
            host=config["MYSQL_HOST"],
            port=config["MYSQL_PORT"],
            user=config["MYSQL_USER"],
            password=config["MYSQL_PASSWORD"],
            database=config["MYSQL_DATABASE"],
        )

    raise ValueError(
        f"Unknown STORAGE_BACKEND '{backend}'. Use 'mysql' or 'google_sheets'."
    )
