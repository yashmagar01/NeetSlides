"""
NeetSlides CLI - Command-line interface for PDF to PPTX conversion.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="neetslides",
    help="Convert AI-generated slide PDFs into fully editable PowerPoint files.",
    add_completion=False,
)
console = Console()


def version_callback(value: bool) -> None:
    """Display version information."""
    if value:
        from neetslides import __version__
        console.print(f"[bold blue]NeetSlides[/bold blue] version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """
    NeetSlides - Convert AI-generated slide PDFs into editable PPTX files.
    
    Uses semantic reconstruction to intelligently extract titles, bullets,
    and hierarchy from PDF slides and generate properly structured PowerPoint
    files with native placeholders.
    """
    pass


@app.command()
def convert(
    input_pdf: Path = typer.Argument(
        ...,
        help="Path to the input PDF file.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        help="Path for the output PPTX file. Defaults to input filename with .pptx extension.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-V",
        help="Enable verbose output for debugging.",
    ),
) -> None:
    """
    Convert a PDF slide deck to an editable PPTX file.
    
    Example:
        neetslides convert slides.pdf -o output.pptx
    """
    # Determine output path
    if output is None:
        output = input_pdf.with_suffix(".pptx")
    
    console.print(
        Panel(
            f"[bold]Input:[/bold] {input_pdf}\n[bold]Output:[/bold] {output}",
            title="[bold blue]NeetSlides[/bold blue]",
            subtitle="PDF → PPTX Conversion",
        )
    )
    
    if verbose:
        console.print("[dim]Verbose mode enabled[/dim]")
    
    # TODO: Implement conversion pipeline
    # Phase 1: Parse PDF with pdfplumber
    # Phase 2: Apply semantic heuristics
    # Phase 3: Generate PPTX with python-pptx
    
    console.print(
        "[yellow]⚠️  Conversion engine not yet implemented.[/yellow]\n"
        "[dim]This is a Phase 0 skeleton. Full implementation coming in Phases 1-3.[/dim]"
    )


@app.command()
def info(
    input_pdf: Path = typer.Argument(
        ...,
        help="Path to the PDF file to analyze.",
        exists=True,
        file_okay=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
    ),
    json_output: bool = typer.Option(
        False,
        "--json",
        "-j",
        help="Output as JSON for machine processing.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-V",
        help="Show detailed text block information.",
    ),
) -> None:
    """
    Display information about a PDF file without converting.
    
    Useful for debugging and understanding PDF structure.
    """
    import json
    
    from rich.table import Table
    from rich.tree import Tree
    
    from neetslides.parser import get_pdf_info, parse_pdf
    
    console.print(f"[bold]Analyzing:[/bold] {input_pdf}\n")
    
    try:
        info_data = get_pdf_info(input_pdf)
        
        if json_output:
            console.print_json(json.dumps(info_data, indent=2))
            return
        
        # Display summary
        console.print(
            Panel(
                f"[bold]Pages:[/bold] {info_data['total_pages']}\n"
                f"[bold]Text Blocks:[/bold] {info_data['total_text_blocks']}",
                title=f"[bold blue]{input_pdf.name}[/bold blue]",
            )
        )
        
        # Font histogram
        if info_data["font_sizes"]:
            console.print("\n[bold]Font Size Distribution:[/bold]")
            table = Table(show_header=True)
            table.add_column("Size (pt)", style="cyan")
            table.add_column("Count", style="green")
            for size, count in sorted(info_data["font_sizes"].items(), reverse=True):
                table.add_row(f"{size}", f"{count}")
            console.print(table)
        
        # Verbose: show text blocks per page
        if verbose:
            doc = parse_pdf(input_pdf)
            console.print("\n[bold]Text Blocks by Page:[/bold]")
            
            for slide in doc.slides:
                tree = Tree(f"[bold cyan]Page {slide.page_num + 1}[/bold cyan] ({slide.width:.0f}x{slide.height:.0f})")
                for block in slide.text_blocks:
                    size_info = f"[dim]{block.font_size:.1f}pt[/dim]" if block.font_size else ""
                    # Truncate long text
                    text = block.text[:60] + "..." if len(block.text) > 60 else block.text
                    tree.add(f"{text} {size_info}")
                console.print(tree)
                console.print()
        
        # PDF Metadata
        if info_data["metadata"]:
            console.print("\n[bold]PDF Metadata:[/bold]")
            for key, value in info_data["metadata"].items():
                console.print(f"  [dim]{key}:[/dim] {value}")
                
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
