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
    from rich.progress import Progress, SpinnerColumn, TextColumn
    
    from neetslides.generator import convert_pdf_to_pptx
    from neetslides.heuristics import analyze_document
    from neetslides.parser import parse_pdf
    
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
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            # Phase 1: Parse PDF
            task = progress.add_task("Parsing PDF...", total=None)
            doc = parse_pdf(input_pdf)
            progress.update(task, description=f"[green]✓[/green] Parsed {doc.total_pages} pages")
            
            # Check for image-only PDF (no extractable text)
            total_blocks = len(doc.get_all_text_blocks())
            if total_blocks == 0:
                progress.stop()
                console.print(
                    "\n[bold yellow]⚠️  Warning: No extractable text found![/bold yellow]\n\n"
                    "This PDF appears to contain only images (possibly a scanned document,\n"
                    "screenshot-based export, or slides saved as images).\n\n"
                    "[bold]NeetSlides works best with:[/bold]\n"
                    "  • PDFs exported directly from presentation software\n"
                    "  • AI-generated PDFs from NotebookLM, ChatGPT, etc.\n"
                    "  • Born-digital PDFs with selectable text\n\n"
                    "[dim]Tip: Try opening the PDF and check if you can select/copy text.\n"
                    "If not, the PDF is image-based and requires OCR (not yet supported).[/dim]"
                )
                raise typer.Exit(1)
            
            if verbose:
                console.print(f"[dim]  Text blocks: {total_blocks}[/dim]")
            
            # Phase 2: Analyze semantics
            task2 = progress.add_task("Analyzing slide structure...", total=None)
            analyzed = analyze_document(doc)
            progress.update(task2, description="[green]✓[/green] Semantic analysis complete")
            
            if verbose:
                for slide in analyzed.slides:
                    title = slide.title or "(no title)"
                    console.print(f"[dim]  Page {slide.page_num + 1}: {title}[/dim]")
            
            # Phase 3: Generate PPTX
            task3 = progress.add_task("Generating PPTX...", total=None)
            from neetslides.generator.pptx_generator import generate_pptx
            generate_pptx(analyzed, output)
            progress.update(task3, description="[green]✓[/green] PPTX generated")
        
        console.print(f"\n[bold green]✓ Success![/bold green] Output saved to: {output}")
        
    except Exception as e:
        console.print(f"\n[bold red]✗ Error:[/bold red] {e}")
        if verbose:
            import traceback
            console.print(f"[dim]{traceback.format_exc()}[/dim]")
        raise typer.Exit(1)


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
