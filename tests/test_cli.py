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
    assert "NeetSlides" in result.stdout
    assert "0.1.0" in result.stdout


def test_help():
    """Test that --help flag works."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "NeetSlides" in result.stdout
    assert "convert" in result.stdout


def test_convert_missing_file():
    """Test convert command with non-existent file."""
    result = runner.invoke(app, ["convert", "nonexistent.pdf"])
    assert result.exit_code != 0


# TODO: Add more tests as implementation progresses
