## jogger_to_pdf.py

Generate a PDF book from all Jogger blog posts.

### Usage

```bash
# Generate jogger.pdf in the repo root
./util/jogger_to_pdf.py

# Specify output location
./util/jogger_to_pdf.py -o /path/to/my-jogger.pdf

# Save the intermediate markdown file for debugging
./util/jogger_to_pdf.py --temp-md jogger-combined.md
```

### Requirements

- **pandoc** - Install with `brew install pandoc`
- **LaTeX** (for PDF generation) - Install with `brew install --cask mactex-no-gui`

### What it does

1. Collects all markdown files from `content/jogger/`
2. Sorts them chronologically by date from frontmatter
3. Combines them into a single markdown document
4. Converts to PDF using pandoc with:
   - Table of contents
   - A4 paper size
   - 1 inch margins
   - Each post as a separate chapter

### Output

The generated PDF includes:
- All 172+ blog posts in chronological order
- Post titles as chapter headings
- Publication dates
- Full content including formatting
- Page breaks between posts
