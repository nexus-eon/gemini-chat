# Gemini Chat Application

A modern, interactive chat application using Google's Gemini AI model, featuring both CLI and web interfaces.

## Features

- 🌐 Modern web interface with real-time chat
- 🚀 Modern Python packaging with PDM and `pyproject.toml`
- 🔒 Secure environment variable handling
- 📝 Rich terminal output with markdown support
- 🎨 Type hints and validation with Pydantic
- 📊 Structured logging with `structlog`
- 🖥️ User-friendly CLI interface with `typer`
- ⚡ Async-ready architecture
- 🔄 Rate limit handling and user feedback
- 🐛 Comprehensive error handling and logging
- ✨ Code quality tools (ruff, black, isort)
- 🧪 Testing with pytest

## Prerequisites

- Python 3.9 or higher
- [PDM](https://pdm.fming.dev/) package manager

## Installation

### 1. Install PDM (if not already installed)

```bash
# Using pip
pip install --user pdm

# On macOS using Homebrew
brew install pdm

# On Linux using your package manager
# Example for Ubuntu/Debian:
sudo apt install pdm
```

### 2. Clone and Install

```bash
# Clone the repository
git clone https://github.com/yourusername/gemini-chat.git
cd gemini-chat

# Install dependencies and create virtual environment
pdm install
```

### 3. Set up your environment

Create a `.env` file with the following content:

```bash
GEMINI_API_KEY=your_api_key_here
MODEL_NAME=gemini-pro
LOG_LEVEL=INFO
```

Replace `your_api_key_here` with your actual [Google AI Studio API key](https://makersuite.google.com/app/apikey).

## Usage

### Web Interface

Start the web interface with:

```bash
pdm run start-web
```

Options:
- `--host`: Host to bind to (default: 0.0.0.0)
- `--port`, `-p`: Port to bind to (default: 5000)
- `--debug`, `-d`: Enable debug mode

Then open <http://localhost:5000> in your browser.

### CLI Interface

Start the CLI chat application:

```bash
pdm run start
```

Options:
- `--debug`: Enable debug logging
- `--version`: Show version information

## Development

This project uses modern Python development tools and practices:

### Core Dependencies
- **Flask**: Web framework for the chat interface
- **Pydantic**: Data validation and settings management
- **Typer**: Type-safe command line interfaces
- **Rich**: Beautiful terminal formatting
- **structlog**: Structured logging
- **google-generativeai**: Google's Gemini AI API

### Development Tools
- **PDM**: Modern Python package manager
- **mypy**: Static type checking
- **pytest**: Testing framework
- **ruff**: Fast Python linter
- **black**: Code formatter
- **isort**: Import sorter

### Development Commands

```bash
# Install development dependencies
pdm install --dev

# Run type checking
pdm run mypy

# Run tests
pdm run test

# Run linting
pdm run lint

# Format code
pdm run format

# Start web interface in debug mode
pdm run start-web --debug
```

## Project Structure

```plaintext
gemini_chat/
├── src/
│   └── gemini_chat/
│       ├── __init__.py      # Package initialization
│       ├── __main__.py      # Entry point
│       ├── cli.py           # CLI implementation
│       ├── web.py           # Web interface
│       ├── chat.py          # Core chat functionality
│       ├── config.py        # Configuration management
│       ├── py.typed         # Type checking marker
│       ├── static/          # Web static files
│       │   ├── script.js
│       │   └── style.css
│       └── templates/       # Web templates
│           └── index.html
├── tests/                   # Test directory
├── .env                     # Local environment variables
├── .env.example            # Example environment file
├── .gitignore              # Git ignore patterns
├── mypy.ini                # Type checking configuration
├── pyproject.toml          # Project configuration
├── pdm.lock                # Lock file for dependencies
└── README.md               # This file
```

## Error Handling

The application includes comprehensive error handling for:
- Rate limiting from the Gemini API
- Network connectivity issues
- Invalid API keys or configuration
- Malformed requests
- Server errors

Each error is properly logged with context and presented to the user with helpful messages.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`pdm run test && pdm run lint`)
5. Commit your changes (`git commit -m 'feat: add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

MIT License - See LICENSE file for details
