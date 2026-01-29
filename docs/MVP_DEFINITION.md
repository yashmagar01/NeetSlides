# NeetSlides — MVP Definition

> **Version:** 0.1.0\
> **Status:** Phase 0 — Project Alignment

---

## What MVP Includes

### Core Functionality

- ✅ CLI command to convert a single PDF to PPTX
- ✅ Extraction of text content from AI-generated PDFs
- ✅ Detection of slide titles (via font size heuristics)
- ✅ Detection of bullet points and basic hierarchy
- ✅ Generation of PPTX with Title/Body placeholders
- ✅ Support for theme reflow (output uses placeholders, not textboxes)

### User Experience

- ✅ Clear progress indication during conversion
- ✅ Verbose/debug mode for troubleshooting
- ✅ Actionable error messages

### Documentation

- ✅ Installation instructions
- ✅ Usage examples
- ✅ Known limitations documented

---

## What MVP Explicitly Excludes

### Features NOT in v0.1

- ❌ Image extraction or embedding
- ❌ Table reconstruction
- ❌ Chart/diagram preservation
- ❌ Animation support
- ❌ Custom theme/template selection
- ❌ Batch processing (multiple files)
- ❌ GUI or web interface
- ❌ AI-powered content enhancement
- ❌ Cloud deployment or API

### Technical Boundaries

- ❌ Scanned PDFs (OCR not included)
- ❌ Complex multi-column layouts
- ❌ Non-Latin character support (may work but untested)

---

## Success Metrics

| Metric                        | Target                                        |
| ----------------------------- | --------------------------------------------- |
| Title detection accuracy      | ≥80%                                          |
| Bullet hierarchy preservation | ≥80%                                          |
| Theme reflow integrity        | Output maintains structure when theme applied |
| Installation success          | Single `pip install` works                    |
| Conversion time               | <5 seconds for typical 20-slide PDF           |

---

## Target PDF Sources

The MVP is optimized for:

- Google NotebookLM exports
- ChatGPT-generated slides (PDF export)
- Copilot presentation PDFs
- Any "born-digital" AI-generated slide PDF

---

## Out of Scope Rationale

| Excluded Feature | Reason                                                         |
| ---------------- | -------------------------------------------------------------- |
| Images           | Requires separate extraction pipeline, adds complexity         |
| Tables           | Complex semantic reconstruction, defer to future version       |
| GUI              | CLI-first for developer audience, GUI can wrap CLI later       |
| Cloud            | Privacy-first philosophy, local execution only                 |
| OCR              | Focus on born-digital PDFs, scanned docs are different problem |
