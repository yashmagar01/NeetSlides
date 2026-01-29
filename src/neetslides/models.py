"""
NeetSlides Data Models - Pydantic models for structured PDF and slide data.

These models represent the intermediate data structures used throughout
the parsing and generation pipeline.
"""

from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    """Represents a bounding box for a text element."""
    
    x0: float = Field(..., description="Left edge x-coordinate")
    y0: float = Field(..., description="Top edge y-coordinate")
    x1: float = Field(..., description="Right edge x-coordinate")
    y1: float = Field(..., description="Bottom edge y-coordinate")
    
    @property
    def width(self) -> float:
        """Width of the bounding box."""
        return self.x1 - self.x0
    
    @property
    def height(self) -> float:
        """Height of the bounding box."""
        return self.y1 - self.y0
    
    @property
    def center_x(self) -> float:
        """Center x-coordinate."""
        return (self.x0 + self.x1) / 2
    
    @property
    def center_y(self) -> float:
        """Center y-coordinate."""
        return (self.y0 + self.y1) / 2


class TextBlock(BaseModel):
    """Represents a block of text extracted from a PDF page."""
    
    text: str = Field(..., description="The text content")
    font_name: Optional[str] = Field(None, description="Font name/family")
    font_size: Optional[float] = Field(None, description="Font size in points")
    bbox: BoundingBox = Field(..., description="Bounding box coordinates")
    page_num: int = Field(..., description="Page number (0-indexed)")
    
    # Computed during semantic analysis (Phase 2)
    semantic_type: Optional[str] = Field(
        None, 
        description="Semantic type: 'title', 'body', 'bullet', 'header', 'footer'"
    )
    indent_level: int = Field(0, description="Indentation level for bullets")
    
    @property
    def is_bold(self) -> bool:
        """Check if font appears to be bold based on name."""
        if self.font_name is None:
            return False
        name_lower = self.font_name.lower()
        return "bold" in name_lower or "heavy" in name_lower


class SlideData(BaseModel):
    """Represents a single parsed slide/page."""
    
    page_num: int = Field(..., description="Page number (0-indexed)")
    width: float = Field(..., description="Page width in points")
    height: float = Field(..., description="Page height in points")
    text_blocks: list[TextBlock] = Field(
        default_factory=list,
        description="List of text blocks on this page"
    )
    
    # Computed during semantic analysis (Phase 2)
    title: Optional[str] = Field(None, description="Detected slide title")
    body_blocks: list[TextBlock] = Field(
        default_factory=list,
        description="Body text blocks after semantic analysis"
    )


class DocumentData(BaseModel):
    """Represents a complete parsed PDF document."""
    
    source_path: Path = Field(..., description="Path to source PDF")
    total_pages: int = Field(..., description="Total number of pages")
    slides: list[SlideData] = Field(
        default_factory=list,
        description="List of parsed slides"
    )
    
    # Document-level metadata
    pdf_metadata: dict = Field(
        default_factory=dict,
        description="PDF metadata (title, author, etc.)"
    )
    
    def get_all_text_blocks(self) -> list[TextBlock]:
        """Get all text blocks from all slides."""
        blocks = []
        for slide in self.slides:
            blocks.extend(slide.text_blocks)
        return blocks
    
    def get_font_histogram(self) -> dict[float, int]:
        """
        Get histogram of font sizes across all text blocks.
        Useful for title detection heuristics.
        """
        histogram: dict[float, int] = {}
        for block in self.get_all_text_blocks():
            if block.font_size is not None:
                size = round(block.font_size, 1)
                histogram[size] = histogram.get(size, 0) + 1
        return histogram
