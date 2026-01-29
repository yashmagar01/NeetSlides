"""
NeetSlides Generator Module - PPTX reconstruction engine.

This module generates editable PowerPoint files using python-pptx,
with proper semantic placeholders for titles and body content.
"""

from neetslides.generator.pptx_generator import (
    convert_pdf_to_pptx,
    generate_pptx,
    create_presentation,
    add_slide_from_data,
)

__all__ = [
    "convert_pdf_to_pptx",
    "generate_pptx",
    "create_presentation",
    "add_slide_from_data",
]
