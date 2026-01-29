"""
NeetSlides Heuristics Module - Semantic reconstruction engine.

This module applies heuristics to extract semantic meaning from
raw PDF layout data, including title detection, bullet hierarchy,
and artifact removal.
"""

from neetslides.heuristics.semantic_analyzer import (
    analyze_document,
    analyze_slide,
    classify_text_blocks,
    detect_body_font_size,
    detect_bullet_hierarchy,
    detect_title_font_size,
    is_likely_header_footer,
)

__all__ = [
    "analyze_document",
    "analyze_slide",
    "classify_text_blocks",
    "detect_body_font_size",
    "detect_bullet_hierarchy",
    "detect_title_font_size",
    "is_likely_header_footer",
]
