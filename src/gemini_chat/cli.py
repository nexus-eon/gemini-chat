"""Command-line interface for the chat application."""
import logging
import sys
from typing import Any, Optional

import structlog
import typer
from rich.console import Console
from rich.prompt import Prompt

from . import __version__
from .chat import ChatSession
from .config import get_settings

app = typer.Typer(help="Interactive chat application using Google's Gemini AI model")
console = Console()
logger = structlog.get_logger()


def version_callback(value: bool) -> None:
    """Print version information."""
    if value:
        console.print(f"Gemini Chat v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version information and exit.",
        callback=version_callback,
        is_eager=True,
    )
) -> None:
    """Gemini Chat - Interactive AI Chat Application."""
    pass


@app.command()
def chat(
    debug: bool = typer.Option(False, "--debug", "-d", help="Enable debug logging")
) -> None:
    """Start an interactive chat session."""
    # Configure logging
    log_level = logging.DEBUG if debug else logging.INFO
    structlog.configure(
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
    )
    
    try:
        settings = get_settings()
        session = ChatSession(settings)
        
        console.print("\n[bold blue]Welcome to Gemini Chat![/bold blue]")
        console.print("Type 'exit' to end the conversation or 'Ctrl+C' to quit.\n")
        
        while True:
            try:
                user_input = Prompt.ask("[cyan]You[/cyan]")
                
                if user_input.lower() == "exit":
                    console.print("\n[bold blue]Goodbye![/bold blue]")
                    break
                
                response = session.send_message(user_input)
                session.display_message(response)
                
            except KeyboardInterrupt:
                console.print("\n[bold blue]Chat session terminated.[/bold blue]")
                sys.exit(0)
                
    except Exception as e:
        logger.error("chat_error", error=str(e))
        console.print(f"\n[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    app()
