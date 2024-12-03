"""Test web interface functionality."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from flask import Flask, Response
from flask.testing import FlaskClient
from werkzeug.wrappers import Response as WerkzeugResponse

from gemini_chat.web import create_app


@pytest.fixture
def app() -> Flask:
    """Create a test Flask application."""
    return create_app()


@pytest.fixture
def client(app: Flask) -> FlaskClient[Response]:
    """Create a test client."""
    return app.test_client()


def test_index_route(client: FlaskClient[Response]) -> None:
    """Test the index route."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'html' in response.data.lower()


def test_chat_route_get(client: FlaskClient[Response]) -> None:
    """Test that GET requests to /chat are not allowed."""
    response = client.get('/chat')
    assert response.status_code == 405  # Method Not Allowed


def test_chat_route_post_success(client: FlaskClient[Response]) -> None:
    """Test successful chat message handling."""
    with patch('gemini_chat.chat.ChatSession') as mock_chat:
        # Set up the mock
        instance = mock_chat.return_value
        instance.send_message = AsyncMock(return_value="Test response")

        # Make the request
        response = client.post('/chat', json={'message': 'Hello'})

        # Check the response
        assert response.status_code == 200
        assert response.json == {'response': 'Test response'}

        # Verify the mock was called correctly
        instance.send_message.assert_called_once_with('Hello')


def test_chat_route_post_error(client: FlaskClient[Response]) -> None:
    """Test error handling in chat route."""
    with patch('gemini_chat.chat.ChatSession') as mock_chat:
        # Set up the mock to raise an exception
        instance = mock_chat.return_value
        instance.send_message = AsyncMock(side_effect=Exception("Test error"))

        # Make the request
        response = client.post('/chat', json={'message': 'Hello'})

        # Check the response
        assert response.status_code == 500
        assert response.json == {'error': 'Test error'}


def test_chat_route_invalid_json(client: FlaskClient[Response]) -> None:
    """Test handling of invalid JSON in request."""
    response = client.post('/chat', data='invalid json')
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid JSON'}


def test_chat_route_missing_message(client: FlaskClient[Response]) -> None:
    """Test handling of missing message in request."""
    response = client.post('/chat', json={})
    assert response.status_code == 400
    assert response.json == {'error': 'Message is required'}
