import os
import sys
from pathlib import Path
from time import time
import logging

# Set up project root and system path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from deepdoc.parser.html_parser import RAGFlowHtmlParser

# Logging setup
logging.basicConfig(level=logging.INFO)

# Define a clear separator for output sections/chunks
SECTION_SEPARATOR = "\n" + "="*80 + "\n"

def run_html_parser(html_name: str):
    start_time = time()
    
    # 1. Determine Input Path (CORRECTED PATH)
    input_path = PROJECT_ROOT / "input" / f"{html_name}.html"
    
    if not input_path.exists():
        print(f"Error: {input_path} not found. Place HTML file in input/.")
        return

    print(f"Parsing {input_path} using RAGFlowHtmlParser...")
    
    # Read file as binary. The parser handles decoding internally using find_codec/chardet.
    with open(input_path, "rb") as f:
        binary_data = f.read()
    
    # 2. Instantiate parser
    parser = RAGFlowHtmlParser()
    
    # 3. Call the parser (passing binary data)
    sections = parser(fnm=None, binary=binary_data)
    
    elapsed = time() - start_time
    print(f"Done in {elapsed:.2f}s.")
    
    # 4. Process and Save Sections
    output_content = SECTION_SEPARATOR.join(sections)
    
    print(f"Total processed sections/chunks: {len(sections)}")
    
    # Save sections (CORRECTED PATH)
    output_sections = PROJECT_ROOT / "output" / f"sections_{html_name}.txt"
    output_sections.parent.mkdir(exist_ok=True)
    with open(output_sections, "w", encoding="utf-8") as f:
        f.write(output_content)
    print(f"Saved processed sections and tables: {output_sections}")
    
    print("\nAll outputs saved to output/ — check the text file for chunked content and embedded HTML tables.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_html_parser.py <html_file_name_stem_without_extension>")
        print("Example: python ruparser/run_html_parser.py web_report")
        sys.exit(1)
    run_html_parser(sys.argv[1])