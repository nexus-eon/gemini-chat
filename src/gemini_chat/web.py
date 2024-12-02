from flask import Flask, render_template, request, jsonify
from .chat import ChatSession
from .config import Settings
import logging
from typing import Any
import google.api_core.exceptions

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
settings = Settings()
chat = ChatSession(settings)

@app.route('/')
def home() -> str:
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message() -> tuple[Any, int]:
    try:
        message = request.json.get('message', '')
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        try:
            logger.debug("Sending message to Gemini: %s", message)
            response = chat.send_message(message)
            if not response:
                logger.error("Empty response received from Gemini")
                return jsonify({'error': 'Failed to get response from Gemini'}), 500
                
            logger.debug("Received response from Gemini: %s", response)
            return jsonify({'response': response}), 200
        except google.api_core.exceptions.ResourceExhausted as e:
            logger.warning("Rate limit exceeded: %s", str(e))
            return jsonify({
                'error': 'Rate limit exceeded. Please try again in about an hour.',
                'rate_limited': True
            }), 429
            
    except Exception as e:
        logger.error("Error in send_message: %s", str(e))
        return jsonify({'error': 'An error occurred while processing your message'}), 500

def run_web_app() -> None:
    app.run(debug=True, host='0.0.0.0', port=5000)
