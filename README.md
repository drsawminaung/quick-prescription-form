# 📋 Quick Prescription Form

A web tool for physicians to quickly generate patient prescriptions and send them via Telegram bot.

## ✨ Features

- 📝 Clean and intuitive prescription entry form
- 📤 Instant prescription delivery via Telegram
- 📦 Lightweight Flask-based web application
- 🔒 Secure environment variable configuration
- 🎨 Modern, responsive UI design

## 🛠️ Prerequisites

- Python 3.8 or higher
- A Telegram Bot (created via @BotFather)
- Telegram Chat ID (where prescriptions will be sent)

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/drsawminaung/quick-prescription-form.git
cd quick-prescription-form
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Telegram Bot

1. Create a bot using [@BotFather](https://t.me/BotFather) on Telegram
2. Copy your bot token
3. Get your Chat ID by sending a message to your bot and visiting:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
4. Create a `.env` file in the project root:

```bash
cp .env.example .env
```

5. Edit `.env` and add your credentials:

```
TELEGRAM_BOT_TOKEN=your_actual_bot_token_here
TELEGRAM_CHAT_ID=your_actual_chat_id_here
```

### 4. Run the application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 📝 Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Fill in the prescription form with:
   - Patient name and age
   - Diagnosis
   - Medications (with dosage instructions)
   - General instructions
   - Doctor's name
3. Click "Send Prescription"
4. The prescription will be sent to your configured Telegram chat

## 💾 Project Structure

```
quick-prescription-form/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
├── templates/
│   └── form.html          # Prescription form HTML
└── README.md             # This file
```

## 🔧 Configuration

All configuration is done through environment variables in the `.env` file:

- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token from @BotFather
- `TELEGRAM_CHAT_ID`: The chat ID where prescriptions will be sent

## 📚 API Endpoints

### `GET /`
Displays the prescription entry form.

### `POST /send-prescription`
Processes and sends the prescription via Telegram.

**Request Body (JSON):**
```json
{
  "patient_name": "string",
  "patient_age": "number",
  "diagnosis": "string",
  "medications": "string",
  "instructions": "string",
  "doctor_name": "string"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Prescription sent successfully!"
}
```

## 🔒 Security Notes

- Never commit your `.env` file to version control
- Keep your Telegram bot token secure
- The `.gitignore` file is configured to exclude `.env` files

## 🐛 Troubleshooting

**Issue: Telegram bot not configured error**
- Make sure your `.env` file exists and contains valid credentials
- Verify your bot token is correct
- Ensure your chat ID is valid

**Issue: Import errors**
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python version compatibility

## 📝 License

This project is open source and available for use.

## 👨‍⚕️ Author

Created for physicians to streamline prescription delivery.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

---

**Note:** This tool is designed for legitimate medical prescription management. Ensure compliance with local healthcare regulations.
