import os
import sys
from pathlib import Path
from time import time
import logging

# Add root to path for imports (adjust if needed)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# ⚠️ ASSUMPTION: The RAGFlowDocxParser is in deepdoc.parser.docx_parser
# This mirrors the deepdoc.parser.pdf_parser import in run_pdf_parser.py
from deepdoc.parser.docx_parser import RAGFlowDocxParser

# Logging setup
logging.basicConfig(level=logging.INFO)

def run_docx_parser(docx_name: str):
    start_time = time()
    
    # 1. Read DOCX from input/
    input_path = Path("input") / f"{docx_name}.docx"
    if not input_path.exists():
        print(f"Error: {input_path} not found. Place DOCX in input/.")
        return
    
    # Read as binary, as the parser supports Document(BytesIO(fnm))
    with open(input_path, "rb") as f:
        binary_data = f.read()
    
    print(f"Parsing {docx_name} using RAGFlowDocxParser...")
    
    # 2. Instantiate parser
    parser = RAGFlowDocxParser()
    
    # 3. Call the parser (no vision params needed for docx)
    # Returns: secs (list of (text, style)) and tbls (list of table content strings)
    secs, tbls = parser(binary_data)
    
    elapsed = time() - start_time
    print(f"Done in {elapsed:.2f}s.")
    
    # 4. Process and Save Sections (Text/Paragraphs)
    # Format: <tag>text content</tag>
    formatted_sections = []
    for text, style in secs:
        if text.strip():
            # Use the style name as a simple tag, default to <p>
            tag = style.replace(" ", "_") if style else "p"
            formatted_sections.append(f"<{tag}>{text}</{tag}>")

    filtered_text = "\n\n".join(formatted_sections)
    
    print(f"Text blocks: {len(secs)}")
    print(f"Tables: {len(tbls)}")
    
    output_sections = Path("output") / f"sections_{docx_name}.txt"
    output_sections.parent.mkdir(exist_ok=True)
    with open(output_sections, "w", encoding="utf-8") as f:
        f.write(filtered_text)
    print(f"Saved sections (with tags): {output_sections}")
    
    # 5. Process and Save Tables
    tables_dir = Path("output") / f"tables_{docx_name}"
    tables_dir.mkdir(exist_ok=True)
    
    for i, table_content_list in enumerate(tbls):
        # table_content_list is a list of strings (lines/rows)
        table_text = "\n".join(table_content_list)
        
        # Save as a plain text file for simple inspection
        table_path = tables_dir / f"table_{i}.txt"
        with open(table_path, "w", encoding="utf-8") as f:
            f.write(table_text)
        print(f"Saved table {i}: {table_path}")
    
    print("All outputs saved to output/")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_docx_parser.py <docx_name_without_extension>")
        sys.exit(1)
    run_docx_parser(sys.argv[1])