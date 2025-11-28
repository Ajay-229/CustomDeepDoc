import os
import sys
from pathlib import Path
from time import time
import logging

# Set up environment path to find deepdoc modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# ASSUMPTION: The RAGFlowExcelParser is located at deepdoc.parser.excel_parser
# Adjust this import path if your internal file structure dictates a different location
from deepdoc.parser.excel_parser import RAGFlowExcelParser

# Logging setup
logging.basicConfig(level=logging.INFO)

def run_excel_parser(file_name_stem: str):
    start_time = time()
    
    # 1. Determine Input Path (Check for .xlsx then .csv)
    input_dir = Path("input")
    input_path_xlsx = input_dir / f"{file_name_stem}.xlsx"
    input_path_csv = input_dir / f"{file_name_stem}.csv"
    
    input_path = None
    ext = None
    
    if input_path_xlsx.exists():
        input_path = input_path_xlsx
        ext = ".xlsx"
    elif input_path_csv.exists():
        input_path = input_path_csv
        ext = ".csv"
    else:
        print(f"Error: Neither {file_name_stem}.xlsx nor {file_name_stem}.csv found in input/.")
        return

    print(f"Parsing {input_path} (Format: {ext}) using RAGFlowExcelParser...")
    
    # Read as binary, as the parser's internal methods handle file-like objects
    with open(input_path, "rb") as f:
        binary_data = f.read()
    
    # 2. Instantiate parser
    parser = RAGFlowExcelParser()
    
    # 3. Call the parser's __call__ method
    # The __call__ method returns a list of processed text lines (one line per row)
    res = parser(binary_data)
    
    elapsed = time() - start_time
    print(f"Done in {elapsed:.2f}s.")
    
    # 4. Process and Save Sections (Text/Rows)
    # The output is joined by a newline, retaining the original row/sheet context
    filtered_text = "\n".join(res)
    
    print(f"Total processed lines/rows: {len(res)}")
    
    output_sections = Path("output") / f"sections_{file_name_stem}.txt"
    output_sections.parent.mkdir(exist_ok=True)
    with open(output_sections, "w", encoding="utf-8") as f:
        f.write(filtered_text)
    print(f"Saved sections: {output_sections}")
    
    print("\nAll outputs saved to output/ — check the sections text file for processed rows.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_excel_parser.py <file_name_stem_without_extension>")
        print("Example: python run_excel_parser.py sales_data")
        sys.exit(1)
    run_excel_parser(sys.argv[1])