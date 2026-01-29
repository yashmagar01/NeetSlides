"""
Tests for NeetSlides PDF Parser.
"""

from pathlib import Path

import pytest

from neetslides.models import BoundingBox, DocumentData, SlideData, TextBlock


class TestBoundingBox:
    """Tests for BoundingBox model."""
    
    def test_dimensions(self):
        """Test width and height calculations."""
        bbox = BoundingBox(x0=10, y0=20, x1=110, y1=70)
        assert bbox.width == 100
        assert bbox.height == 50
    
    def test_center(self):
        """Test center point calculations."""
        bbox = BoundingBox(x0=0, y0=0, x1=100, y1=100)
        assert bbox.center_x == 50
        assert bbox.center_y == 50


class TestTextBlock:
    """Tests for TextBlock model."""
    
    def test_is_bold_detection(self):
        """Test bold font detection from name."""
        block = TextBlock(
            text="Test",
            font_name="Arial-Bold",
            font_size=12,
            bbox=BoundingBox(x0=0, y0=0, x1=100, y1=20),
            page_num=0,
        )
        assert block.is_bold is True
        
        block2 = TextBlock(
            text="Test",
            font_name="Arial",
            font_size=12,
            bbox=BoundingBox(x0=0, y0=0, x1=100, y1=20),
            page_num=0,
        )
        assert block2.is_bold is False
    
    def test_no_font_name(self):
        """Test is_bold with no font name."""
        block = TextBlock(
            text="Test",
            font_name=None,
            font_size=12,
            bbox=BoundingBox(x0=0, y0=0, x1=100, y1=20),
            page_num=0,
        )
        assert block.is_bold is False


class TestDocumentData:
    """Tests for DocumentData model."""
    
    def test_font_histogram(self):
        """Test font histogram generation."""
        blocks = [
            TextBlock(
                text="Title",
                font_size=24,
                bbox=BoundingBox(x0=0, y0=0, x1=100, y1=30),
                page_num=0,
            ),
            TextBlock(
                text="Body 1",
                font_size=12,
                bbox=BoundingBox(x0=0, y0=50, x1=100, y1=70),
                page_num=0,
            ),
            TextBlock(
                text="Body 2",
                font_size=12,
                bbox=BoundingBox(x0=0, y0=80, x1=100, y1=100),
                page_num=0,
            ),
        ]
        
        slide = SlideData(
            page_num=0,
            width=612,
            height=792,
            text_blocks=blocks,
        )
        
        doc = DocumentData(
            source_path=Path("test.pdf"),
            total_pages=1,
            slides=[slide],
        )
        
        histogram = doc.get_font_histogram()
        assert histogram[24.0] == 1
        assert histogram[12.0] == 2


# Note: Integration tests with actual PDF parsing require
# sample PDF files. Add those tests when sample PDFs are available.
