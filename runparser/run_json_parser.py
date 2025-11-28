import os
import sys
from pathlib import Path
from time import time
import logging

# Set up project root and system path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# ⚠️ ASSUMPTION: The RAGFlowJsonParser is located at deepdoc.parser.json_parser
from deepdoc.parser.json_parser import RAGFlowJsonParser

# Logging setup
logging.basicConfig(level=logging.INFO)

def run_json_parser(file_name_stem: str):
    start_time = time()
    
    # 1. Determine Input Path (Check for .json then .jsonl)
    input_path_json = PROJECT_ROOT / "input" / f"{file_name_stem}.json"
    input_path_jsonl = PROJECT_ROOT / "input" / f"{file_name_stem}.jsonl"
    
    input_path = None
    ext = None
    
    if input_path_json.exists():
        input_path = input_path_json
        ext = ".json"
    elif input_path_jsonl.exists():
        input_path = input_path_jsonl
        ext = ".jsonl"
    else:
        print(f"Error: Neither {file_name_stem}.json nor {file_name_stem}.jsonl found in input/.")
        return

    print(f"Parsing {input_path} (Format: {ext}) using RAGFlowJsonParser...")
    
    # Read as binary, as the parser handles decoding internally
    with open(input_path, "rb") as f:
        binary_data = f.read()
    
    # 2. Instantiate parser
    # Use default chunk sizes (2000 chars * 2 = 4000 max, 3800 min)
    parser = RAGFlowJsonParser() 
    
    # 3. Call the parser's __call__ method
    # The __call__ method returns a list of JSON-formatted string chunks.
    sections = parser(binary_data)
    
    elapsed = time() - start_time
    print(f"Done in {elapsed:.2f}s.")
    
    # 4. Process and Save Sections (JSON Chunks)
    # The output is joined by a newline, with each line being a JSON string chunk
    filtered_text = "\n\n".join(sections)
    
    print(f"Total JSON chunks generated: {len(sections)}")
    
    # Save sections
    output_sections = PROJECT_ROOT / "output" / f"sections_{file_name_stem}.txt"
    output_sections.parent.mkdir(exist_ok=True)
    with open(output_sections, "w", encoding="utf-8") as f:
        f.write(filtered_text)
    print(f"Saved JSON chunks: {output_sections}")
    
    print("\nAll outputs saved to output/ — check the text file for the chunked JSON/JSONL content.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_json_parser.py <file_name_stem_without_extension>")
        print("Example: python ruparser/run_json_parser.py user_data")
        sys.exit(1)
    run_json_parser(sys.argv[1])