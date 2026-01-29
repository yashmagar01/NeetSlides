"""
NeetSlides PDF Parser - Extract structured text and layout from PDFs.

Uses pdfplumber to extract text blocks with font and position metadata
from AI-generated slide PDFs.
"""

from pathlib import Path
from typing import Optional

import pdfplumber
from pdfplumber.page import Page

from neetslides.models import BoundingBox, DocumentData, SlideData, TextBlock


def _extract_text_blocks(page: Page, page_num: int) -> list[TextBlock]:
    """
    Extract text blocks from a PDF page with font and position metadata.
    
    Groups characters by line and extracts dominant font info.
    """
    blocks: list[TextBlock] = []
    
    # Extract words with their bounding boxes
    words = page.extract_words(
        keep_blank_chars=False,
        x_tolerance=3,
        y_tolerance=3,
        extra_attrs=["fontname", "size"],
    )
    
    if not words:
        return blocks
    
    # Group words into lines based on y-coordinate proximity
    lines: list[list[dict]] = []
    current_line: list[dict] = []
    last_top: Optional[float] = None
    y_tolerance = 5  # Points tolerance for same line
    
    # Sort words by y position (top), then x position
    sorted_words = sorted(words, key=lambda w: (w["top"], w["x0"]))
    
    for word in sorted_words:
        if last_top is None or abs(word["top"] - last_top) <= y_tolerance:
            current_line.append(word)
        else:
            if current_line:
                lines.append(current_line)
            current_line = [word]
        last_top = word["top"]
    
    if current_line:
        lines.append(current_line)
    
    # Convert lines to TextBlocks
    for line_words in lines:
        if not line_words:
            continue
        
        # Combine words into line text
        text = " ".join(w["text"] for w in line_words)
        
        # Get bounding box for entire line
        x0 = min(w["x0"] for w in line_words)
        y0 = min(w["top"] for w in line_words)
        x1 = max(w["x1"] for w in line_words)
        y1 = max(w["bottom"] for w in line_words)
        
        # Get dominant font (most common in line)
        font_names = [w.get("fontname") for w in line_words if w.get("fontname")]
        font_sizes = [w.get("size") for w in line_words if w.get("size")]
        
        font_name = font_names[0] if font_names else None
        font_size = font_sizes[0] if font_sizes else None
        
        block = TextBlock(
            text=text.strip(),
            font_name=font_name,
            font_size=font_size,
            bbox=BoundingBox(x0=x0, y0=y0, x1=x1, y1=y1),
            page_num=page_num,
        )
        
        if block.text:  # Only add non-empty blocks
            blocks.append(block)
    
    return blocks


def parse_pdf(pdf_path: Path) -> DocumentData:
    """
    Parse a PDF file and extract structured slide data.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        DocumentData containing all parsed slides
        
    Raises:
        FileNotFoundError: If PDF file doesn't exist
        ValueError: If file is not a valid PDF
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")
    
    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a PDF file: {pdf_path}")
    
    slides: list[SlideData] = []
    pdf_metadata: dict = {}
    
    with pdfplumber.open(pdf_path) as pdf:
        # Extract PDF metadata
        if pdf.metadata:
            pdf_metadata = {k: v for k, v in pdf.metadata.items() if v}
        
        # Process each page
        for page_num, page in enumerate(pdf.pages):
            text_blocks = _extract_text_blocks(page, page_num)
            
            slide = SlideData(
                page_num=page_num,
                width=float(page.width),
                height=float(page.height),
                text_blocks=text_blocks,
            )
            slides.append(slide)
    
    return DocumentData(
        source_path=pdf_path,
        total_pages=len(slides),
        slides=slides,
        pdf_metadata=pdf_metadata,
    )


def get_pdf_info(pdf_path: Path) -> dict:
    """
    Get summary information about a PDF file.
    
    Returns a dict with page count, dimensions, and text block statistics.
    """
    doc = parse_pdf(pdf_path)
    
    all_blocks = doc.get_all_text_blocks()
    font_histogram = doc.get_font_histogram()
    
    return {
        "source": str(doc.source_path),
        "total_pages": doc.total_pages,
        "total_text_blocks": len(all_blocks),
        "font_sizes": dict(sorted(font_histogram.items(), reverse=True)),
        "metadata": doc.pdf_metadata,
        "pages": [
            {
                "page": slide.page_num + 1,
                "dimensions": f"{slide.width:.0f}x{slide.height:.0f}",
                "text_blocks": len(slide.text_blocks),
            }
            for slide in doc.slides
        ],
    }
