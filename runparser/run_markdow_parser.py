import os
import sys
from pathlib import Path
from time import time
import logging

# ====================================================================
# PATH FIX: Set up project root and system path for nested script
# ====================================================================

# PROJECT_ROOT is two levels up from this script (mydeepdoc/)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import the parser
from deepdoc.parser.markdown_parser import RAGFlowMarkdownParser

# Logging setup
logging.basicConfig(level=logging.INFO)

# Define a clear separator for output sections/chunks
SECTION_SEPARATOR = "\n" + "="*80 + "\n"

def run_markdown_parser(md_name: str):
    start_time = time()
    
    # 1. Determine Input Path (Check for .md then .markdown - CORRECTED PATHS)
    input_path_md = PROJECT_ROOT / "input" / f"{md_name}.md"
    input_path_markdown = PROJECT_ROOT / "input" / f"{md_name}.markdown"
    
    input_path = None
    
    if input_path_md.exists():
        input_path = input_path_md
    elif input_path_markdown.exists():
        input_path = input_path_markdown
    else:
        print(f"Error: Neither {md_name}.md nor {md_name}.markdown found in input/.")
        return

    print(f"Parsing {input_path.name} using RAGFlowMarkdownParser...")
    
    # Read file as binary. The parser handles decoding internally.
    with open(input_path, "rb") as f:
        binary_data = f.read()
    
    # 2. Instantiate parser
    parser = RAGFlowMarkdownParser()
    
    # 3. Call the parser (passing binary data)
    # The fix is in the RAGFlowMarkdownParser class: it must have a __call__ method.
    # Assuming the fixed RAGFlowMarkdownParser is used:
    sections = parser(binary_data)
    
    elapsed = time() - start_time
    print(f"Done in {elapsed:.2f}s.")
    
    # 4. Process and Save Sections
    output_content = SECTION_SEPARATOR.join(sections)
    
    print(f"Total processed sections/chunks: {len(sections)}")
    
    # Save sections (CORRECTED PATH)
    output_sections = PROJECT_ROOT / "output" / f"sections_{md_name}.txt"
    output_sections.parent.mkdir(exist_ok=True)
    with open(output_sections, "w", encoding="utf-8") as f:
        f.write(output_content)
    print(f"Saved processed sections and tables: {output_sections}")
    
    print("\nAll outputs saved to output/ — check the text file for chunked content.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_markdown_parser.py <markdown_file_name_stem_without_extension>")
        print("Example: python ruparser/run_markdown_parser.py documentation")
        sys.exit(1)
    run_markdown_parser(sys.argv[1])