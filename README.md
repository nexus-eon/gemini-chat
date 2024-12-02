# Gemini Chat Application

A modern, interactive chat application using Google's Gemini AI model, featuring both CLI and web interfaces.

## Features

- 🌐 Modern web interface with real-time chat
- 🚀 Modern Python packaging with `pyproject.toml`
- 🔒 Secure environment variable handling
- 📝 Rich terminal output with markdown support
- 🎨 Type hints and validation with Pydantic
- 📊 Structured logging
- 🖥️ User-friendly CLI interface
- ⚡ Async-ready architecture
- 🔄 Rate limit handling and user feedback
- 🐛 Comprehensive error handling and logging

## Prerequisites

- Python 3.12 or higher
- Virtual environment

## Installation

### 1. Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
venv\Scripts\activate  # On Windows
```

### 2. Install the package in editable mode

```bash
pip install -e .
```

### 3. Set up your environment

Create a `.env` file with the following content:

```bash
GEMINI_API_KEY=your_api_key_here
MODEL_NAME=gemini-exp-1121
LOG_LEVEL=INFO
```

Replace `your_api_key_here` with your actual Gemini API key.

## Usage

### Web Interface

Start the web interface:

```bash
python -m gemini_chat web
```

Then open http://localhost:5000 in your browser.

### CLI Interface

Start the CLI chat application:

```bash
python -m gemini_chat chat
```

Options:

- `--debug`: Enable debug logging
- `--version`: Show version information

## Development

This project uses modern Python development tools:

- **Flask**: Web framework
- **Pydantic**: Data validation and settings management
- **Typer**: CLI interface
- **Rich**: Terminal formatting
- **structlog**: Structured logging
- **mypy**: Static type checking

### Development Commands

```bash
# Run type checking
mypy src/gemini_chat

# Install in development mode
pip install -e .

# Run the web interface in debug mode
python -m gemini_chat web --debug
```

## Project Structure

```
gemini_chat/
├── src/
│   └── gemini_chat/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py          # CLI implementation
│       ├── web.py         # Web interface
│       ├── chat.py        # Core chat functionality
│       ├── config.py      # Configuration management
│       ├── static/        # Web static files
│       │   ├── script.js
│       │   └── style.css
│       └── templates/     # Web templates
│           └── index.html
├── .env                  # Environment variables
├── .gitignore
├── README.md
└── setup.py             # Package configuration
```

## Error Handling

The application includes comprehensive error handling for:
- Rate limiting from the Gemini API
- Network issues
- Invalid API keys
- Malformed requests
- Server errors

## License

MIT License
