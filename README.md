# GoTech Solutions - Contact Form Backend (Python)

A small Flask API that replaces the Google Apps Script approach with a real
backend you control. It supports **two interchangeable storage backends** —
switch between them with one setting, no code changes needed:

- `mysql` — saves each submission as a row in a MySQL table.
- `google_sheets` — saves each submission as a row in a Google Sheet, using
  a service account (no manual Apps Script deployment required).

```
backend/
├── app.py                 Flask app + routes (POST /api/contact, etc.)
├── config.py               Loads settings from .env
├── validation.py           Server-side input validation
├── storage/
│   ├── base.py              Common interface both backends implement
│   ├── mysql_storage.py     MySQL backend (PyMySQL, auto-creates table)
│   └── google_sheets_storage.py  Google Sheets backend (gspread)
├── schema.sql               MySQL schema (optional, for manual setup)
├── requirements.txt
├── .env.example
└── README.md                 This file
```

## 1. Install dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## 2. Choose and configure a storage backend

Open `.env` and set `STORAGE_BACKEND` to either `mysql` or `google_sheets`,
then fill in the matching section below.

### Option A — MySQL

1. Have a MySQL server available (local install, Docker, or a managed
   service like PlanetScale, Railway, or RDS).
2. Either let the app create the table automatically on first run, or run
   `schema.sql` yourself:
   ```bash
   mysql -u root -p < schema.sql
   ```
3. Fill in `MYSQL_HOST`, `MYSQL_PORT`, `MYSQL_USER`, `MYSQL_PASSWORD`,
   `MYSQL_DATABASE` in `.env`.

### Option B — Google Sheets (service account, no Apps Script)

1. In [Google Cloud Console](https://console.cloud.google.com/), create a
   project (or use an existing one) and enable the **Google Sheets API**.
2. Create a **Service Account** (IAM & Admin → Service Accounts), then
   create a JSON key for it and download it.
3. Save the JSON key as `backend/service-account.json` (or set
   `GOOGLE_SERVICE_ACCOUNT_FILE` to wherever you put it). **Never commit
   this file** — it grants access to whatever you share with it.
4. Create a Google Sheet (e.g. "GoTech Contact Submissions"), then **share
   it** with the service account's email address (the `client_email` field
   inside the JSON key) with **Editor** access.
5. Copy the Sheet ID from its URL —
   `https://docs.google.com/spreadsheets/d/<THIS_PART>/edit` — into
   `GOOGLE_SHEET_ID` in `.env`.
6. The app creates a `Submissions` worksheet and header row automatically
   on first run if they don't exist.

## 3. Run it locally

```bash
python app.py
```

The API is now live at `http://localhost:5000`. Check it with:

```bash
curl http://localhost:5000/api/health
```

## 4. Point the website at this API

In `assets/js/main.js`, set:

```js
const CONTACT_API_URL = "http://localhost:5000/api/contact";
```

and for production, once deployed, your live API URL, e.g.
`https://api.gotechsolutions.co.ke/api/contact` or
`https://gotech-backend.onrender.com/api/contact`.

Also add your website's origin(s) to `ALLOWED_ORIGINS` in `.env` so the
browser's CORS check allows the request (e.g. your GitHub Pages URL and any
custom domain).

## 5. API reference

### `POST /api/contact`

Body (JSON or form-encoded):

```json
{
  "name": "Jane Doe",
  "email": "jane@company.com",
  "phone": "+254700000000",
  "service": "Web Development & UI/UX Design",
  "message": "I need a new business website...",
  "page": "https://gotechsolutions.co.ke/contact.html"
}
```

Responses:

- `201` — `{"status": "success", "id": "42"}`
- `400` — `{"status": "error", "message": "...", "field": "email"}` (validation failure)
- `502` — `{"status": "error", "message": "..."}` (storage backend unreachable)

### `GET /api/health`

Returns `{"status": "ok", "backend": "mysql"}` — useful for uptime checks.

### `GET /api/submissions?limit=50`

Returns the most recent submissions. Protected: requires header
`X-API-Key: <ADMIN_API_KEY>` matching the value set in `.env`. Disabled
(returns 401) if `ADMIN_API_KEY` is left blank.

## 6. Deploying

This is a standard Flask app, so it runs on any Python host:

- **Render / Railway** — connect the repo, set the start command to
  `gunicorn app:app`, add the `.env` values as environment variables in the
  dashboard (don't upload `.env` itself), and for Google Sheets, add
  `service-account.json` as a secret file.
- **A VPS** — run behind `gunicorn` + nginx:
  ```bash
  gunicorn -w 2 -b 0.0.0.0:5000 app:app
  ```
- **Docker** — wrap the above in a small Dockerfile if you prefer containers.

The static site itself (GitHub Pages) doesn't need to change beyond the
`CONTACT_API_URL` in `main.js` and the `ALLOWED_ORIGINS` on the backend.

## 7. Switching backends later

Because both backends implement the same `SubmissionStorage` interface
(see `storage/base.py`), switching from Google Sheets to MySQL (or back)
later is just changing `STORAGE_BACKEND` in `.env` and restarting — no
application code changes needed.
