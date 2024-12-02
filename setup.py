"""Setup file for development installation."""
from setuptools import setup

setup(
    name="gemini-chat",
    package_dir={"": "src"},
    packages=["gemini_chat"],
    install_requires=[
        "google-generativeai>=0.3.0",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "typer>=0.9.0",
        "pydantic>=2.6.1",
        "pydantic-settings>=2.0.0",
        "structlog>=24.1.0",
        "flask>=3.0.0",
    ],
)
