"""
GoTech Solutions - Contact Form Backend
========================================
A small Flask API that receives contact-form submissions from the website
and stores them in either Google Sheets or MySQL, depending on the
STORAGE_BACKEND setting in your .env file.

Run locally:
    pip install -r requirements.txt
    cp .env.example .env      # then fill in the values
    python app.py

The API exposes:
    POST /api/contact   -> validates + stores a submission
    GET  /api/health     -> simple health check
    GET  /api/submissions (optional, protected by API key) -> list recent submissions

See README.md for full setup instructions (Google Sheets AND MySQL).
"""

import logging
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from config import Config
from storage import get_storage_backend
from validation import ValidationError, validate_submission

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("gotech.backend")


def create_app(config_object: type = Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    # Allow the static site (GitHub Pages, localhost, etc.) to call this API.
    allowed_origins = app.config["ALLOWED_ORIGINS"]
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

    # Storage backend is chosen once at startup based on STORAGE_BACKEND
    # ("google_sheets" or "mysql") and reused for every request.
    storage = get_storage_backend(app.config)
    app.extensions = getattr(app, "extensions", {})
    app.extensions["storage"] = storage

    register_routes(app)
    register_error_handlers(app)
    return app


def register_routes(app: Flask) -> None:
    @app.get("/api/health")
    def health():
        return jsonify(
            status="ok",
            backend=app.config["STORAGE_BACKEND"],
        )

    @app.post("/api/contact")
    def submit_contact():
        storage = app.extensions["storage"]

        payload = request.get_json(silent=True) or request.form.to_dict()

        try:
            clean = validate_submission(payload)
        except ValidationError as exc:
            return jsonify(status="error", message=str(exc), field=exc.field), 400

        clean["page"] = clean.get("page") or request.headers.get("Referer", "")
        clean["ip_address"] = request.headers.get(
            "X-Forwarded-For", request.remote_addr
        )

        try:
            record_id = storage.save_submission(clean)
        except Exception:
            logger.exception("Failed to persist contact submission")
            return (
                jsonify(
                    status="error",
                    message="We could not save your message right now. Please try again shortly or email us directly.",
                ),
                502,
            )

        logger.info("Saved contact submission id=%s from %s", record_id, clean["email"])
        return jsonify(status="success", id=record_id), 201

    @app.get("/api/submissions")
    def list_submissions():
        # Lightweight protection so this endpoint isn't wide open. Set
        # ADMIN_API_KEY in .env and pass it as X-API-Key to use this.
        api_key = app.config.get("ADMIN_API_KEY")
        if not api_key or request.headers.get("X-API-Key") != api_key:
            return jsonify(status="error", message="Unauthorized"), 401

        storage = app.extensions["storage"]
        limit = min(int(request.args.get("limit", 50)), 500)
        return jsonify(status="success", submissions=storage.list_submissions(limit=limit))


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(404)
    def not_found(_err):
        return jsonify(status="error", message="Not found"), 404

    @app.errorhandler(500)
    def server_error(_err):
        return jsonify(status="error", message="Internal server error"), 500


app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
