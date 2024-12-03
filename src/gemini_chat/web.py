"""Web interface for the chat application."""
from typing import Optional, Union, Tuple, Dict, Any, cast

import structlog
from flask import Flask, Response, jsonify, render_template, request
from werkzeug.exceptions import BadRequest

from .chat import ChatSession, RateLimitError
from .config import Settings, get_settings

logger = structlog.get_logger()

# Type alias for Flask JSON responses
JSONResponse = Union[Response, Tuple[Response, int]]


def create_app(settings: Optional[Settings] = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config['settings'] = settings or get_settings()

    @app.route('/')
    def index() -> str:
        """Render the chat interface."""
        return render_template('index.html')

    @app.route('/chat', methods=['POST'])
    def chat() -> JSONResponse:
        """Handle chat messages."""
        try:
            if not request.is_json or not request.get_data():
                logger.warning("bad_request", error="Invalid JSON")
                return cast(JSONResponse, (jsonify({'error': "Invalid JSON"}), 400))

            try:
                data: Dict[str, Any] = request.get_json()
            except BadRequest:
                logger.warning("bad_request", error="Invalid JSON")
                return cast(JSONResponse, (jsonify({'error': "Invalid JSON"}), 400))

            if not data or 'message' not in data:
                logger.warning("bad_request", error="Message is required")
                return cast(JSONResponse, (jsonify({'error': "Message is required"}), 400))

            message: str = data['message']
            logger.debug("received_message", message=message)

            chat_session = ChatSession(settings=app.config['settings'])
            response: str = chat_session.send_message(message)

            return cast(JSONResponse, jsonify({'response': response}))

        except RateLimitError as e:
            logger.warning("rate_limit_error", error=str(e))
            return cast(JSONResponse, (jsonify({
                'error': str(e),
                'rate_limited': True
            }), 429))

        except BadRequest as e:
            logger.warning("bad_request", error=str(e))
            return cast(JSONResponse, (jsonify({'error': str(e)}), 400))

        except Exception as e:
            logger.error("chat_error", error=str(e))
            return cast(JSONResponse, (jsonify({'error': str(e)}), 500))

    return app


def run_app(host: str = '0.0.0.0', port: int = 5000, debug: bool = False) -> None:
    """Run the Flask application."""
    app = create_app()
    app.run(host=host, port=port, debug=debug)
