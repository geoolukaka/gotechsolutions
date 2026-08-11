from abc import ABC, abstractmethod


class SubmissionStorage(ABC):
    """Common interface every storage backend (MySQL, Google Sheets, ...)
    must implement, so app.py never needs to know which one is active."""

    @abstractmethod
    def save_submission(self, data: dict) -> str:
        """Persist a validated submission dict and return a record id/string."""
        raise NotImplementedError

    @abstractmethod
    def list_submissions(self, limit: int = 50) -> list:
        """Return the most recent submissions, newest first."""
        raise NotImplementedError
