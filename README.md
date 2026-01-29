# NeetSlides

> **Convert AI-generated slide PDFs into fully editable PowerPoint files.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## The Problem

AI tools like **NotebookLM**, **ChatGPT**, and **Copilot** generate beautiful
slide decks—but often export them as PDFs. This creates real problems for
students and educators:

- ❌ **No editability** — Can't modify content, fix errors, or personalize
  slides
- ❌ **Template lock-in** — Can't apply institutional or academic templates
- ❌ **Accessibility issues** — PDFs often lack proper semantic structure
- ❌ **Rubric non-compliance** — Many courses require editable PPTX submissions

Existing PDF-to-PPTX converters either produce garbled output, require cloud
uploads (privacy concern), or cost money.

## The Solution

**NeetSlides** uses semantic reconstruction to convert AI-generated PDFs into
clean, editable PowerPoint files:

- ✅ **Semantic extraction** — Intelligently detects titles, bullets, and
  hierarchy
- ✅ **Native placeholders** — Uses proper PPTX Title/Body placeholders
- ✅ **Theme-ready** — Output files reflow correctly when templates are applied
- ✅ **100% local** — No cloud uploads, no telemetry, your data stays private
- ✅ **Open source** — Apache 2.0 licensed, free forever

---

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/neetslides.git
cd neetslides

# Install in development mode
pip install -e .
```

## Quick Start

```bash
# Convert a single PDF
neetslides convert slides.pdf -o output.pptx

# Convert with verbose output
neetslides convert slides.pdf -o output.pptx --verbose
```

---

## How It Works

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐     ┌────────────┐
│   PDF       │ ──► │  Parse & Extract │ ──► │ Semantic        │ ──► │  Generate  │
│   Input     │     │  (pdfplumber)    │     │ Heuristics      │     │  PPTX      │
└─────────────┘     └──────────────────┘     └─────────────────┘     └────────────┘
                           │                        │                      │
                    Text, fonts,              Title detection,       Native placeholders,
                    bounding boxes            bullet hierarchy       theme-ready output
```

### Key Principles

1. **Semantic Reconstruction** — We don't try to visually clone the PDF.
   Instead, we extract _meaning_ (titles, bullets, hierarchy) and reconstruct it
   properly.

2. **Born-Digital Focus** — Optimized for AI-generated PDFs which have
   consistent, predictable layouts.

3. **Academic-First** — Designed for student workflows, academic rubrics, and
   institutional templates.

---

## Roadmap

| Phase | Description                    | Status         |
| ----- | ------------------------------ | -------------- |
| 0     | Project Alignment & Guardrails | 🔄 In Progress |
| 1     | PDF Parsing Engine             | ⏳ Planned     |
| 2     | Semantic Heuristics Engine     | ⏳ Planned     |
| 3     | PPTX Reconstruction Engine     | ⏳ Planned     |
| 4     | CLI Experience & Developer UX  | ⏳ Planned     |
| 5     | Academic Validation & QA       | ⏳ Planned     |
| 6     | Open-Source Release            | ⏳ Planned     |

---

## Tech Stack

| Component       | Library       | License |
| --------------- | ------------- | ------- |
| PDF Parsing     | `pdfplumber`  | MIT     |
| PPTX Generation | `python-pptx` | MIT     |
| CLI Framework   | `typer`       | MIT     |
| Terminal UX     | `rich`        | MIT     |

> **Note:** We explicitly avoid AGPL-licensed dependencies (e.g., PyMuPDF) to
> maintain license compatibility.

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for
guidelines.

---

## License

Apache 2.0 — See [LICENSE](LICENSE) for details.

---

## Acknowledgments

Built by [Yash](https://github.com/YOUR_USERNAME) with engineering support from
Antigravity.
