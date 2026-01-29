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
) -> None:
    """
    Display information about a PDF file without converting.
    
    Useful for debugging and understanding PDF structure.
    """
    console.print(f"[bold]Analyzing:[/bold] {input_pdf}")
    
    # TODO: Implement PDF analysis
    console.print(
        "[yellow]⚠️  Analysis engine not yet implemented.[/yellow]\n"
        "[dim]This is a Phase 0 skeleton. Full implementation coming in Phase 1.[/dim]"
    )


if __name__ == "__main__":
    app()
