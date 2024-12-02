# Gemini Chat Application

A modern, interactive chat application using Google's Gemini AI model.

## Features

- 🚀 Modern Python packaging with `pyproject.toml`
- 🔒 Secure environment variable handling
- 📝 Rich terminal output with markdown support
- 🎨 Type hints and validation with Pydantic
- 📊 Structured logging
- 🖥️ User-friendly CLI interface
- ⚡ Async-ready architecture

## Prerequisites

- Python 3.9 or higher
- PDM (Python package manager)

## Installation

### 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows
```

### 2. Install PDM if you haven't already

```bash
pip install pdm
```

### 3. Install the project dependencies

```bash
pdm install
```

### 4. Set up your environment

```bash
cp .env.example .env
```

Then edit `.env` and add your Gemini API key.

## Usage

Start the chat application:

```bash
pdm run python -m gemini_chat.cli chat
```

Options:

- `--debug`: Enable debug logging
- `--version`: Show version information

## Development

This project uses modern Python development tools:

- **PDM**: Dependency management
- **Ruff**: Fast Python linter
- **Black**: Code formatting
- **isort**: Import sorting
- **Pydantic**: Data validation
- **Typer**: CLI interface
- **Rich**: Terminal formatting
- **structlog**: Structured logging

### Development Commands

```bash
# Format code
pdm run black .
pdm run isort .

# Lint code
pdm run ruff check .

# Run tests (when added)
pdm run pytest
```

## License

MIT License
