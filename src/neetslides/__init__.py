"""
NeetSlides - Convert AI-generated slide PDFs into editable PowerPoint files.

This package provides a CLI tool and library for semantic reconstruction
of slide content from PDF to PPTX format.
"""

__version__ = "0.1.0"
__author__ = "Yash"
__license__ = "Apache-2.0"

from neetslides.cli import app

__all__ = ["app", "__version__"]
