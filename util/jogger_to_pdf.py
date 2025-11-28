#!/usr/bin/env python3
"""
Generate a PDF from all Jogger blog posts.

This script uses Hugo to generate a special single-page HTML with all jogger posts,
then converts it to PDF using weasyprint (preferred) or wkhtmltopdf.

Dependencies:
- hugo (already installed)
- weasyprint (pip install weasyprint) OR
- wkhtmltopdf (brew install wkhtmltopdf)
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime

def create_book_content_file(content_dir):
    """Create a content file that uses the book layout."""
    book_file = Path(content_dir) / 'jogger-book.md'
    with open(book_file, 'w', encoding='utf-8') as f:
        f.write('---\n')
        f.write('title: "Jogger Book"\n')
        f.write('layout: book\n')
        f.write('type: jogger\n')
        f.write('draft: true\n')  # Exclude from normal builds
        f.write('---\n')
    return book_file


def generate_html_with_hugo(repo_root):
    """Generate HTML using Hugo with the book layout."""
    print("Generating HTML with Hugo...")

    # Run Hugo
    cmd = ['hugo', '-D']
    try:
        subprocess.run(cmd, cwd=repo_root, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running hugo: {e}")
        print(e.stderr.decode())
        return None

    # Find the generated HTML
    html_file = repo_root / 'public' / 'jogger-book' / 'index.html'
    if not html_file.exists():
        print(f"Error: Expected HTML not found at {html_file}")
        return None

    return html_file


def html_to_pdf_weasyprint(html_file, pdf_file):
    """Convert HTML to PDF using weasyprint."""
    try:
        from weasyprint import HTML
        print("Using weasyprint for PDF conversion...")
        HTML(filename=str(html_file)).write_pdf(str(pdf_file))
        return True
    except ImportError:
        return False
    except Exception as e:
        print(f"Error with weasyprint: {e}")
        return False


def html_to_pdf_wkhtmltopdf(html_file, pdf_file):
    """Convert HTML to PDF using wkhtmltopdf."""
    cmd = [
        'wkhtmltopdf',
        '--enable-local-file-access',
        '--print-media-type',
        '--margin-top', '20mm',
        '--margin-bottom', '20mm',
        '--margin-left', '20mm',
        '--margin-right', '20mm',
        str(html_file),
        str(pdf_file)
    ]

    try:
        print("Using wkhtmltopdf for PDF conversion...")
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error running wkhtmltopdf: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Generate PDF from Jogger posts using Hugo')
    parser.add_argument('--output', '-o', default='jogger.pdf',
                        help='Output PDF filename')
    parser.add_argument('--keep-html', action='store_true',
                        help='Keep the generated HTML file')
    parser.add_argument('--html-only', action='store_true',
                        help='Generate HTML only, do not convert to PDF')

    args = parser.parse_args()

    # Find repo root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    content_dir = repo_root / 'content'

    if not content_dir.exists():
        print(f"Error: Content directory not found: {content_dir}")
        sys.exit(1)

    # Create temporary book content file
    print("Creating book content file...")
    book_file = create_book_content_file(content_dir)

    try:
        # Generate HTML with Hugo
        html_file = generate_html_with_hugo(repo_root)
        if not html_file:
            print("✗ Failed to generate HTML")
            sys.exit(1)

        print(f"✓ Generated HTML: {html_file}")

        if args.html_only:
            print("HTML-only mode: skipping PDF conversion")
            return

        # Convert to PDF
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = repo_root / output_path

        print(f"Converting to PDF: {output_path}")

        # Try weasyprint first, fall back to wkhtmltopdf
        success = html_to_pdf_weasyprint(html_file, output_path)
        if not success:
            success = html_to_pdf_wkhtmltopdf(html_file, output_path)

        if not success:
            print("✗ Failed to generate PDF")
            print("Install either:")
            print("  pip install weasyprint")
            print("  OR")
            print("  brew install wkhtmltopdf")
            sys.exit(1)

        print(f"✓ PDF generated successfully: {output_path}")

        # Show file size
        size_mb = output_path.stat().st_size / (1024 * 1024)
        print(f"  File size: {size_mb:.1f} MB")

    finally:
        # Cleanup
        if book_file.exists():
            book_file.unlink()

        if not args.keep_html:
            # Remove generated HTML directory
            html_dir = repo_root / 'public' / 'jogger-book'
            if html_dir.exists():
                import shutil
                shutil.rmtree(html_dir)


if __name__ == '__main__':
    main()
