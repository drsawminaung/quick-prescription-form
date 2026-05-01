"""
Quick Prescription Form
=======================
A Flask web application for physicians to generate and send patient
prescriptions via a Telegram bot.

Routes:
    GET  /                  — Render the prescription form
    POST /send-prescription — Validate, format, and send via Telegram
    GET  /health            — Health check endpoint
"""

import asyncio
import logging
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from telegram import Bot
from telegram.error import TelegramError

# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------
load_dotenv()

logging.basicConfig(
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
REQUIRED_FIELDS = ["patient_name", "patient_age", "diagnosis", "medications", "doctor_name"]


def _validate(data: dict) -> list[str]:
    """Return a list of validation error messages, or empty list if valid."""
    errors: list[str] = []
    for field in REQUIRED_FIELDS:
        if not str(data.get(field, "")).strip():
            label = field.replace("_", " ").title()
            errors.append(f"{label} is required.")

    age = data.get("patient_age", "")
    try:
        age_int = int(age)
        if not (0 <= age_int <= 150):
            errors.append("Patient age must be between 0 and 150.")
    except (ValueError, TypeError):
        if age:  # Only flag if a value was provided but invalid
            errors.append("Patient age must be a number.")

    return errors


def _format_prescription(data: dict) -> str:
    """Build the Telegram message string from form data."""
    now = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    medications = data.get("medications", "").strip()
    instructions = data.get("instructions", "").strip()
    follow_up = data.get("follow_up", "").strip()
    doctor_name = data.get("doctor_name", "").strip()
    clinic_name = data.get("clinic_name", "").strip()

    lines = [
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        "📋  PRESCRIPTION",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"👤  Patient : {data.get('patient_name', '').strip()}",
        f"🎂  Age     : {data.get('patient_age', '').strip()} years",
        f"🏥  Dx      : {data.get('diagnosis', '').strip()}",
        "",
        "💊  MEDICATIONS",
        "─────────────────────────",
        medications,
    ]

    if instructions:
        lines += ["", "📝  INSTRUCTIONS", "─────────────────────────", instructions]

    if follow_up:
        lines += ["", f"🔁  Follow-up : {follow_up}"]

    lines += [
        "",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"👨‍⚕️  Dr. {doctor_name}",
    ]

    if clinic_name:
        lines.append(f"🏢  {clinic_name}")

    lines += [f"🕒  {now}", "━━━━━━━━━━━━━━━━━━━━━━━━"]

    return "\n".join(lines)


async def _send_telegram_message(token: str, chat_id: str, text: str) -> None:
    """Send a message via Telegram asynchronously."""
    bot = Bot(token=token)
    async with bot:
        await bot.send_message(chat_id=chat_id, text=text)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    """Render the prescription form."""
    return render_template("form.html")


@app.route("/health")
def health():
    """Simple health check endpoint."""
    configured = bool(BOT_TOKEN and CHAT_ID)
    return jsonify({"status": "ok", "telegram_configured": configured})


@app.route("/send-prescription", methods=["POST"])
def send_prescription():
    """Validate form data and dispatch the prescription via Telegram."""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"success": False, "message": "Invalid request: expected JSON body."}), 400

    # Server-side validation
    errors = _validate(data)
    if errors:
        return jsonify({"success": False, "message": " ".join(errors)}), 422

    if not BOT_TOKEN or not CHAT_ID:
        logger.warning("Telegram credentials are not configured.")
        return jsonify({"success": False, "message": "Telegram bot is not configured on the server."}), 503

    message = _format_prescription(data)

    try:
        asyncio.run(_send_telegram_message(BOT_TOKEN, CHAT_ID, message))
        patient = data.get("patient_name", "unknown").strip()
        logger.info("Prescription sent for patient: %s", patient)
        return jsonify({"success": True, "message": "Prescription sent successfully!"})
    except TelegramError as exc:
        logger.error("Telegram error: %s", exc)
        return jsonify({"success": False, "message": f"Telegram error: {exc}"}), 502
    except Exception as exc:  # noqa: BLE001
        logger.error("Unexpected error: %s", exc)
        return jsonify({"success": False, "message": "An unexpected error occurred. Please try again."}), 500


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "false").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
