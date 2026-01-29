"""
NeetSlides Semantic Analyzer - Reconstruct meaning from PDF layout.

This module applies heuristics to extract semantic meaning from raw PDF
layout data, including title detection, bullet hierarchy, and artifact removal.
"""

from typing import Optional

from neetslides.models import DocumentData, SlideData, TextBlock


def detect_title_font_size(doc: DocumentData) -> Optional[float]:
    """
    Detect the likely title font size using histogram analysis.
    
    Heuristic: Titles are typically:
    - Larger than body text
    - Used less frequently (one per slide)
    - Near the top of pages
    
    Returns the font size most likely used for titles.
    """
    histogram = doc.get_font_histogram()
    
    if not histogram:
        return None
    
    # Sort by font size descending
    sorted_sizes = sorted(histogram.items(), key=lambda x: x[0], reverse=True)
    
    # The largest font that appears across multiple slides is likely the title
    num_slides = doc.total_pages
    
    for size, count in sorted_sizes:
        # Title should appear roughly once per slide (±50%)
        if 0.5 * num_slides <= count <= 1.5 * num_slides:
            return size
    
    # Fallback: return the largest font size
    return sorted_sizes[0][0] if sorted_sizes else None


def detect_body_font_size(doc: DocumentData, title_size: Optional[float] = None) -> Optional[float]:
    """
    Detect the most common body text font size.
    
    Heuristic: Body text is the most frequently used font size
    that is smaller than the title size.
    """
    histogram = doc.get_font_histogram()
    
    if not histogram:
        return None
    
    # Filter out title size and get most common remaining
    candidates = [
        (size, count) for size, count in histogram.items()
        if title_size is None or size < title_size
    ]
    
    if not candidates:
        return None
    
    # Return the most frequently used body size
    return max(candidates, key=lambda x: x[1])[0]


def classify_text_blocks(slide: SlideData, title_size: float, body_size: float) -> None:
    """
    Classify text blocks as title, body, or other based on font size.
    
    Modifies blocks in-place, setting semantic_type field.
    """
    title_tolerance = 1.0  # points
    
    for block in slide.text_blocks:
        if block.font_size is None:
            block.semantic_type = "body"
            continue
        
        if abs(block.font_size - title_size) < title_tolerance:
            block.semantic_type = "title"
        elif block.font_size >= body_size - 1:
            block.semantic_type = "body"
        else:
            # Smaller text might be footnotes, headers, etc.
            block.semantic_type = "small"


def detect_bullet_hierarchy(blocks: list[TextBlock]) -> None:
    """
    Detect bullet hierarchy based on x-position indentation.
    
    Heuristic: Bullets at similar x-positions are at the same level.
    Deeper indentation = higher indent_level.
    
    Modifies blocks in-place, setting indent_level field.
    """
    if not blocks:
        return
    
    # Get body blocks only
    body_blocks = [b for b in blocks if b.semantic_type == "body"]
    
    if not body_blocks:
        return
    
    # Find the minimum x position (left margin)
    left_margin = min(b.bbox.x0 for b in body_blocks)
    
    # Quantize x-positions into indent levels
    # Typical indent is ~20-30 points
    indent_step = 25.0
    
    for block in body_blocks:
        indent_pixels = block.bbox.x0 - left_margin
        block.indent_level = int(indent_pixels / indent_step)


def is_likely_header_footer(block: TextBlock, slide: SlideData) -> bool:
    """
    Detect if a text block is likely a header or footer.
    
    Heuristics:
    - Very top or bottom of page (within 50 points)
    - Usually small font size
    - Often contains page numbers or dates
    """
    top_margin = 50
    bottom_margin = slide.height - 50
    
    # Check position
    if block.bbox.y0 < top_margin:
        return True  # Header area
    if block.bbox.y1 > bottom_margin:
        return True  # Footer area
    
    # Check for common footer patterns
    text_lower = block.text.lower()
    footer_patterns = ["page", "slide", "©", "copyright", "confidential"]
    for pattern in footer_patterns:
        if pattern in text_lower:
            return True
    
    return False


def analyze_slide(slide: SlideData, title_size: float, body_size: float) -> SlideData:
    """
    Apply semantic analysis to a single slide.
    
    Returns the slide with semantic annotations applied.
    """
    # Classify blocks
    classify_text_blocks(slide, title_size, body_size)
    
    # Detect bullet hierarchy
    detect_bullet_hierarchy(slide.text_blocks)
    
    # Find title block (first title-classified block near top)
    title_blocks = [
        b for b in slide.text_blocks 
        if b.semantic_type == "title"
    ]
    if title_blocks:
        # Sort by y-position, take topmost
        title_blocks.sort(key=lambda b: b.bbox.y0)
        slide.title = title_blocks[0].text
    
    # Collect body blocks (excluding headers/footers)
    slide.body_blocks = [
        b for b in slide.text_blocks
        if b.semantic_type == "body" and not is_likely_header_footer(b, slide)
    ]
    
    return slide


def analyze_document(doc: DocumentData) -> DocumentData:
    """
    Apply semantic analysis to an entire document.
    
    Detects titles, body text, bullet hierarchy, and artifacts.
    Returns the document with semantic annotations applied.
    """
    # Detect font sizes
    title_size = detect_title_font_size(doc)
    body_size = detect_body_font_size(doc, title_size)
    
    # Use defaults if detection failed
    if title_size is None:
        title_size = 24.0  # Common title size
    if body_size is None:
        body_size = 12.0  # Common body size
    
    # Analyze each slide
    for slide in doc.slides:
        analyze_slide(slide, title_size, body_size)
    
    return doc
