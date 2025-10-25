from flask import Flask, render_template, request, jsonify
from telegram import Bot
from telegram.error import TelegramError
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Telegram bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

@app.route('/')
def index():
    """Render the prescription form"""
    return render_template('form.html')

@app.route('/send-prescription', methods=['POST'])
def send_prescription():
    """Process and send prescription via Telegram"""
    try:
        data = request.json
        
        # Extract form data
        patient_name = data.get('patient_name')
        patient_age = data.get('patient_age')
        diagnosis = data.get('diagnosis')
        medications = data.get('medications')
        instructions = data.get('instructions')
        doctor_name = data.get('doctor_name')
        
        # Format prescription message
        message = f"""📋 PRESCRIPTION

👤 Patient: {patient_name}
🎂 Age: {patient_age}
🏥 Diagnosis: {diagnosis}

💊 MEDICATIONS:
{medications}

📝 INSTRUCTIONS:
{instructions}

👨‍⚕️ Prescribed by: Dr. {doctor_name}
"""
        
        # Send via Telegram
        if BOT_TOKEN and CHAT_ID:
            bot = Bot(token=BOT_TOKEN)
            bot.send_message(chat_id=CHAT_ID, text=message)
            logger.info(f"Prescription sent for patient: {patient_name}")
            return jsonify({'success': True, 'message': 'Prescription sent successfully!'})
        else:
            logger.warning('Telegram credentials not configured')
            return jsonify({'success': False, 'message': 'Telegram bot not configured'}), 400
            
    except TelegramError as e:
        logger.error(f"Telegram error: {str(e)}")
        return jsonify({'success': False, 'message': f'Telegram error: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Error sending prescription: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to send prescription'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
