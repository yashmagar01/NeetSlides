"""
NeetSlides Parser Module - PDF parsing and text extraction.

This module handles extraction of text, fonts, and bounding boxes
from AI-generated PDF slides using pdfplumber.
"""

from neetslides.parser.pdf_parser import get_pdf_info, parse_pdf

__all__ = ["parse_pdf", "get_pdf_info"]
