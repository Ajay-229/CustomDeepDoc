import os
import sys
from pathlib import Path
from time import time
import logging

# Set up project root and system path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from deepdoc.parser.excel_parser import RAGFlowExcelParser

# Logging setup
logging.basicConfig(level=logging.INFO)

def run_excel_parser(file_name_stem: str):
    start_time = time()
    
    # 1. Determine Input Path (Check for .xlsx then .csv - CORRECTED PATHS)
    input_path_xlsx = PROJECT_ROOT / "input" / f"{file_name_stem}.xlsx"
    input_path_csv = PROJECT_ROOT / "input" / f"{file_name_stem}.csv"
    
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
    res = parser(binary_data)
    
    elapsed = time() - start_time
    print(f"Done in {elapsed:.2f}s.")
    
    # 4. Process and Save Sections (Text/Rows)
    filtered_text = "\n".join(res)
    
    print(f"Total processed lines/rows: {len(res)}")
    
    # Save sections (CORRECTED PATH)
    output_sections = PROJECT_ROOT / "output" / f"sections_{file_name_stem}.txt"
    output_sections.parent.mkdir(exist_ok=True)
    with open(output_sections, "w", encoding="utf-8") as f:
        f.write(filtered_text)
    print(f"Saved sections: {output_sections}")
    
    print("\nAll outputs saved to output/ — check the sections text file for processed rows.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_excel_parser.py <file_name_stem_without_extension>")
        print("Example: python ruparser/run_excel_parser.py sales_data")
        sys.exit(1)
    run_excel_parser(sys.argv[1])