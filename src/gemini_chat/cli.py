"""Command-line interface for the chat application."""
import logging
import sys
from typing import Optional

import structlog
import typer
from rich.console import Console

from . import __version__
from .chat import ChatSession
from .config import Settings
from .web import run_web_app

app = typer.Typer(help="Interactive chat application using Google's Gemini AI model")
console = Console()
logger = structlog.get_logger()


def version_callback(value: bool) -> None:
    """Show version information and exit."""
    if value:
        console.print(f"Gemini Chat v{__version__}")
        raise typer.Exit()


@app.command()
def chat(debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug logging")) -> None:
    """Start a chat session with Gemini"""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
        
    settings = Settings()
    chat_instance = ChatSession(settings)
    
    console.print("Welcome to Gemini Chat! Type 'exit' to quit.")
    while True:
        message = input("You: ")
        if message.lower() == 'exit':
            break
        
        response = chat_instance.send_message(message)
        console.print(f"\nGemini: {response}\n")


@app.command()
def web() -> None:
    """Start the web interface"""
    console.print("Starting web interface at http://localhost:5000")
    run_web_app()


@app.callback()
def callback(version: Optional[bool] = typer.Option(None, "--version", callback=version_callback, is_eager=True)) -> None:
    """Show version information and exit."""
    pass


def main() -> None:
    """Main entry point for the application."""
    app()


if __name__ == "__main__":
    main()
