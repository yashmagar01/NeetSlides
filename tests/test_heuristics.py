"""
Tests for NeetSlides Semantic Heuristics.
"""

from pathlib import Path

import pytest

from neetslides.heuristics import (
    analyze_document,
    classify_text_blocks,
    detect_body_font_size,
    detect_bullet_hierarchy,
    detect_title_font_size,
)
from neetslides.models import BoundingBox, DocumentData, SlideData, TextBlock


def create_test_document() -> DocumentData:
    """Create a test document with realistic slide structure."""
    slides = []
    
    for page_num in range(3):
        blocks = [
            # Title block (24pt, top of page)
            TextBlock(
                text=f"Slide {page_num + 1} Title",
                font_size=24.0,
                font_name="Arial-Bold",
                bbox=BoundingBox(x0=50, y0=50, x1=500, y1=80),
                page_num=page_num,
            ),
            # Body text (12pt)
            TextBlock(
                text="This is body text line 1",
                font_size=12.0,
                font_name="Arial",
                bbox=BoundingBox(x0=50, y0=120, x1=500, y1=140),
                page_num=page_num,
            ),
            TextBlock(
                text="This is body text line 2",
                font_size=12.0,
                font_name="Arial",
                bbox=BoundingBox(x0=50, y0=150, x1=500, y1=170),
                page_num=page_num,
            ),
            # Indented bullet (12pt, indented)
            TextBlock(
                text="Indented bullet point",
                font_size=12.0,
                font_name="Arial",
                bbox=BoundingBox(x0=80, y0=180, x1=500, y1=200),
                page_num=page_num,
            ),
        ]
        
        slide = SlideData(
            page_num=page_num,
            width=612,
            height=792,
            text_blocks=blocks,
        )
        slides.append(slide)
    
    return DocumentData(
        source_path=Path("test.pdf"),
        total_pages=3,
        slides=slides,
    )


class TestTitleDetection:
    """Tests for title font size detection."""
    
    def test_detect_title_size(self):
        """Test that title font size is correctly detected."""
        doc = create_test_document()
        title_size = detect_title_font_size(doc)
        
        # Should detect 24pt as title (appears 3 times, once per slide)
        assert title_size == 24.0
    
    def test_detect_body_size(self):
        """Test that body font size is correctly detected."""
        doc = create_test_document()
        title_size = detect_title_font_size(doc)
        body_size = detect_body_font_size(doc, title_size)
        
        # Should detect 12pt as body (most common non-title)
        assert body_size == 12.0


class TestTextClassification:
    """Tests for text block classification."""
    
    def test_classify_blocks(self):
        """Test that blocks are classified correctly."""
        doc = create_test_document()
        slide = doc.slides[0]
        
        classify_text_blocks(slide, title_size=24.0, body_size=12.0)
        
        # First block should be title
        assert slide.text_blocks[0].semantic_type == "title"
        
        # Other blocks should be body
        assert slide.text_blocks[1].semantic_type == "body"
        assert slide.text_blocks[2].semantic_type == "body"


class TestBulletHierarchy:
    """Tests for bullet hierarchy detection."""
    
    def test_detect_indent_levels(self):
        """Test that indentation levels are detected."""
        doc = create_test_document()
        slide = doc.slides[0]
        
        # First classify blocks
        classify_text_blocks(slide, title_size=24.0, body_size=12.0)
        
        # Then detect hierarchy
        detect_bullet_hierarchy(slide.text_blocks)
        
        # Body blocks at x=50 should be level 0
        body_at_50 = [b for b in slide.text_blocks if b.bbox.x0 == 50 and b.semantic_type == "body"]
        assert all(b.indent_level == 0 for b in body_at_50)
        
        # Block at x=80 should be indented (level 1)
        indented = [b for b in slide.text_blocks if b.bbox.x0 == 80]
        assert len(indented) == 1
        assert indented[0].indent_level >= 1


class TestDocumentAnalysis:
    """Tests for full document analysis."""
    
    def test_analyze_document(self):
        """Test full document analysis pipeline."""
        doc = create_test_document()
        analyzed = analyze_document(doc)
        
        # Each slide should have a detected title
        for slide in analyzed.slides:
            assert slide.title is not None
            assert "Title" in slide.title
        
        # Each slide should have body blocks
        for slide in analyzed.slides:
            assert len(slide.body_blocks) > 0
