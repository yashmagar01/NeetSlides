"""
Tests for NeetSlides CLI.
"""

import pytest
from typer.testing import CliRunner

from neetslides.cli import app

runner = CliRunner()


def test_version():
    """Test that --version flag works."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    # Rich strips ANSI codes but text should be present
    assert "0.1.0" in result.stdout


def test_help():
    """Test that --help flag works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    # Check for key command and option text
    assert "convert" in result.stdout.lower() or "Convert" in result.stdout


def test_convert_missing_file():
    """Test convert command with non-existent file."""
    result = runner.invoke(app, ["convert", "nonexistent.pdf"])
    assert result.exit_code != 0


# TODO: Add more tests as implementation progresses
