import os
import sys
from io import BytesIO
from pathlib import Path
from time import time
import logging

# Add root to path for imports (adjust if needed)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import from your deepdoc
from deepdoc.parser.pdf_parser import RAGFlowPdfParser
from deepdoc.vision.ocr import OCR  # For any direct use, but parser handles it

# Logging setup
logging.basicConfig(level=logging.INFO)

def run_pdf_parser(pdf_name: str):
    start_time = time()
    
    # Read PDF from input/
    input_path = Path("input") / f"{pdf_name}.pdf"
    if not input_path.exists():
        print(f"Error: {input_path} not found. Place PDF in input/.")
        return
    
    with open(input_path, "rb") as f:
        binary = f.read()
    
    print(f"Parsing {pdf_name} with full Deepdoc vision...")
    
    # Instantiate parser (loads OCR, LayoutRecognizer, TableStructureRecognizer)
    parser = RAGFlowPdfParser()
    
    # Call with full vision: need_image=True for crops, zoomin=3 for quality, return_html=True for tables
    filtered_text, tables = parser(binary, need_image=True, zoomin=3, return_html=True)
    
    elapsed = time() - start_time
    total_pages = len(parser.page_images) if hasattr(parser, 'page_images') else "Unknown"
    
    print(f"Done in {elapsed:.2f}s. Pages: {total_pages}")
    separator = '\n\n'
    print(f"Text blocks: {len(filtered_text.split(separator)) if filtered_text else 0}")
    print(f"Tables/Figures: {len(tables)}")
    
    # Save sections (text with tags)
    output_sections = Path("output") / f"sections_{pdf_name}.txt"
    output_sections.parent.mkdir(exist_ok=True)
    with open(output_sections, "w", encoding="utf-8") as f:
        f.write(filtered_text)
    print(f"Saved sections: {output_sections}")
    
    # Save tables/figures
    tables_dir = Path("output") / f"tables_{pdf_name}"
    tables_dir.mkdir(exist_ok=True)
    figures_dir = Path("output") / f"figures_{pdf_name}"
    figures_dir.mkdir(exist_ok=True)
    
    for i, (img_pil, content) in enumerate(tables):
        if isinstance(content, str) and "<table" in content:  # Table HTML
            html_path = tables_dir / f"table_{i}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(f"<html><body>{content}</body></html>")
            print(f"Saved table {i}: {html_path}")
        elif isinstance(content, list) and content:  # Figure caption
            caption = "\n".join(content)
            img_path = figures_dir / f"figure_{i}.png"
            img_pil.save(img_path)
            print(f"Saved figure {i} (caption: {caption[:50]}...): {img_path}")
        else:
            print(f"Unknown content for item {i}")
    
    print("All outputs saved to output/ — check tables.html in browser, figures.png visually.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_pdf_parser.py <pdf_name_without_extension>")
        sys.exit(1)
    run_pdf_parser(sys.argv[1])