# 📋 Quick Prescription Form

A responsive, mobile-friendly web application for physicians to quickly generate patient prescriptions and send them instantly via a Telegram bot. Built with Flask and `python-telegram-bot` v21.

---

## ✨ Features

- **Modern UI** — Clean, responsive, and accessible form design.
- **Instant Delivery** — Prescriptions are formatted beautifully and sent to your Telegram chat immediately.
- **Robust Validation** — Client-side and server-side validation ensures no missing data.
- **Async Telegram Integration** — Non-blocking Telegram API calls for fast response times.
- **Production Ready** — Configured with Gunicorn and a `Procfile` for easy deployment to Heroku, Render, or Railway.

---

## 🛠️ Prerequisites

- Python 3.11 or higher
- A Telegram Bot token (from [@BotFather](https://t.me/BotFather))
- Your Telegram Chat ID (where prescriptions will be sent)

---

## 🚀 Quick Start (Local Development)

### 1. Clone the repository

```bash
git clone https://github.com/drsawminaung/quick-prescription-form.git
cd quick-prescription-form
```

### 2. Create a virtual environment and install dependencies

```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and fill in your Telegram credentials:
- `TELEGRAM_BOT_TOKEN`: Your bot token.
- `TELEGRAM_CHAT_ID`: Your chat ID. (To find this, message your bot and visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`).

### 4. Run the Flask application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## 🌐 Deployment

This application is ready to be deployed to any PaaS provider (Heroku, Render, Railway, etc.) that supports Python and `Procfile`.

1. Connect your GitHub repository to your PaaS provider.
2. Set the **Environment Variables** (`TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`) in your provider's dashboard.
3. The provider will automatically detect the `Procfile` and start the app using Gunicorn:
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 30
   ```

---

## 🔌 API Endpoints

### `GET /`
Renders the main prescription HTML form.

### `GET /health`
Returns a JSON health check and verifies if Telegram credentials are set.
```json
{
  "status": "ok",
  "telegram_configured": true
}
```

### `POST /send-prescription`
Accepts a JSON payload and sends the prescription via Telegram.

**Request Body:**
```json
{
  "patient_name": "John Doe",
  "patient_age": "45",
  "diagnosis": "Hypertension",
  "medications": "Amlodipine 5mg - 1 tab daily",
  "instructions": "Monitor BP daily",
  "follow_up": "2 weeks",
  "doctor_name": "Saw Min Aung",
  "clinic_name": "City Clinic"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Prescription sent successfully!"
}
```

---

## 📁 Project Structure

```
quick-prescription-form/
├── app.py                # Main Flask application
├── requirements.txt      # Python dependencies
├── Procfile              # Deployment configuration
├── .env.example          # Environment variable template
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── templates/
    └── form.html         # Frontend UI
```

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Built for clinical workflow automation by [@drsawminaung](https://github.com/drsawminaung)*
