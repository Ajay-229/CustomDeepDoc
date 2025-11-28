import os
import sys
from pathlib import Path
from time import time
import logging

# ====================================================================
# PATH FIX: Set up project root and system path for nested script
# ====================================================================

# This assumes the run script is typically located in a subdirectory 
# (e.g., myproject/parser/run_ppt_parser.py), so the project root is two levels up.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import the parser
# NOTE: Update 'deepdoc.parser.ppt_parser' if your file is located elsewhere 
# in the RAGFlow project structure.

from deepdoc.parser.ppt_parser import RAGFlowPptParser


# Logging setup
logging.basicConfig(level=logging.INFO)

# Define a clear separator for output sections/chunks
SECTION_SEPARATOR = "\n" + "="*80 + "\n"

def run_ppt_parser(ppt_name: str):
    """
    Runs the RAGFlowPptParser on a specified PowerPoint file and saves the extracted text.
    """
    start_time = time()
    
    # 1. Determine Input Path (Checks PROJECT_ROOT/input/)
    input_path = PROJECT_ROOT / "input" / f"{ppt_name}.pptx"
    
    if not input_path.exists():
        print(f"Error: {input_path} not found.")
        print("Please ensure the PowerPoint file is in the 'input/' directory.")
        return

    print(f"Parsing {input_path.name} using RAGFlowPptParser...")
    
    # Read file as binary (The parser's __call__ method handles binary via BytesIO)
    with open(input_path, "rb") as f:
        binary_data = f.read()
    
    # 2. Instantiate parser
    parser = RAGFlowPptParser()
    
    # 3. Call the parser
    # The __call__ signature is (fnm, from_page, to_page, callback=None).
    # We use a large number (99999) for 'to_page' to process all slides.
    try:
        sections = parser(binary_data, 0, 99999)
    except Exception as e:
        logging.error(f"Error during parser execution for {ppt_name}.pptx: {e}")
        return
    
    elapsed = time() - start_time
    print(f"Done parsing in {elapsed:.2f}s.")
    
    # 4. Process and Save Sections
    
    # Filter out empty sections (slides that had no extractable text)
    filtered_sections = [s.strip() for s in sections if s.strip()]
    output_content = SECTION_SEPARATOR.join(filtered_sections)
    
    print(f"Total processed sections/slides: {len(filtered_sections)}")
    
    # Save sections (Saves to PROJECT_ROOT/output/)
    output_sections = PROJECT_ROOT / "output" / f"sections_{ppt_name}.txt"
    output_sections.parent.mkdir(exist_ok=True) # Ensure 'output' directory exists
    
    with open(output_sections, "w", encoding="utf-8") as f:
        f.write(output_content)
        
    print(f"Saved extracted text to: {output_sections}")
    
    print("\nCheck the 'output/' directory for the chunked content.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_ppt_parser.py <powerpoint_file_name_stem_without_extension>")
        print("Example: python run_ppt_parser.py annual_report")
        sys.exit(1)
    
    # Run the parser with the filename stem provided as a command-line argument
    run_ppt_parser(sys.argv[1])