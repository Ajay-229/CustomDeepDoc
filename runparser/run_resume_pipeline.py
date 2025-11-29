import os
import sys
import json
import logging
import re
from io import BytesIO
from pathlib import Path
from time import time
import datetime # Required for date calculations (used in the final stage)
import pandas as pd
import numpy as np

# --- 1. SETUP: Configure Environment & Imports ---
# Assumed project structure where 'deepdoc' and 'ruparser' are siblings to the script's location
PROJECT_ROOT = Path(__file__).resolve().parent.parent 
sys.path.insert(0, str(PROJECT_ROOT))

# Only import the components necessary for THIS script (Parsers and core Python libs)
try:
    from deepdoc.parser.pdf_parser import RAGFlowPdfParser
    from deepdoc.parser.docx_parser import RAGFlowDocxParser
except ImportError:
    logging.warning("deepdoc parsers not found. Using internal MockParser for demonstration.")
    class MockParser:
        def __init__(self): pass
        def __call__(self, binary_data, **kwargs):
            # Simulate raw text output from the parser
            return "name: 张三\nwork: 字节跳动 (2018-2023)", []
    RAGFlowPdfParser = RAGFlowDocxParser = MockParser

# Logging setup
logging.basicConfig(level=logging.INFO)

# --- 2. RESUME EXTRACTION & FEATURE ENGINEERING FUNCTION STUBS ---
# NOTE: The actual entity/tokenizer imports (degrees, corporations, rag_tokenizer) are assumed 
# to happen inside the *real* init.py, step1.py, and step2.py files.

def resume_extractor(filtered_text: str) -> dict:
    """Mocks the intermediate model that converts raw parser text into a structured CV dictionary."""
    logging.info("MOCK: Converting raw text into structured resume dictionary.")
    
    return {
        "tob_resume_id": str(time()).replace('.', ''),
        "raw_txt": filtered_text,
        "basic": {
            "name": "张三",
            "birth": "1990-01-01",
            "degree": "7",
        },
        "work": {
            "0": {"corporation_name": "字节跳动", "position_name": "产品经理", "start_time": "2018-06-01", "end_time": "2023-12-31"},
        },
        "education": {
            "0": {"school_name": "清华大学", "degree": "7", "start_time": "2015-09-01", "end_time": "2018-06-01"},
        },
    }

def refactor_init(cv: dict) -> dict:
    """Simulates the logic of init.py: initial cleanup and basic field promotion."""
    cv["is_deleted"] = 0
    if "basic" not in cv: cv["basic"] = {}
    
    work_list = [v for _, v in cv.get("work", {}).items()]
    edu_list = [v for _, v in cv.get("education", {}).items()]
    
    if work_list:
        cv["basic"]["corporation_name"] = work_list[-1].get("corporation_name", "")
    if edu_list:
        cv["basic"]["school_name"] = edu_list[-1].get("school_name", "")

    cv["basic"]["updated_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logging.info("STEP 1/3 (init.py): Initial normalization and basic field promotion completed.")
    return cv

def refactor_step1(cv_dict: dict) -> dict:
    """Mocks the execution of step1.py: Flattening and standardization."""
    # Simulate data flattening and passing to step 2
    cv_dict["corporation_name"] = cv_dict.get("basic", {}).get("corporation_name", "")
    cv_dict["degree"] = "硕士" # Mocks degrees.get_name() usage
    cv_dict["education_obj"] = cv_dict.pop("education", {})
    
    logging.info("STEP 2/3 (step1.py): Dictionary flattening and standardization completed.")
    return cv_dict

def parse_step2(cv: dict) -> dict:
    """Mocks the execution of step2.py: Feature engineering and final suffixing."""
    # Mock date utility for age calculation
    def getYMD(b):
        y = re.search(r"[0-9]{4}", str(b))
        return (int(y.group(0)) if y else 2000, 1, 1)

    # Simplified feature creation logic
    cv["age_int"] = datetime.datetime.now().year - getYMD(cv.get("basic", {}).get("birth", ""))[0]
    cv["highest_degree_kwd"] = cv.get("degree")
    cv["corp_tag_kwd"] = ["互联网"] # Mocks corporations.corp_tag() usage
    cv["corporation_name_tks"] = "zi_jie_tiao_dong_tks" # Mocks rag_tokenizer.tokenize() usage
    
    # Final cleanup and suffixing
    final_features = {}
    for k, v in cv.items():
        if re.search(r"_(fea|tks|nst|dt|int|flt|ltks|kwd|id)$", k) or k in ["tob_resume_id"]:
            final_features[k] = v
            
    final_features["id"] = cv.get("tob_resume_id", "NO_ID")
    
    logging.info("STEP 3/3 (step2.py): Feature engineering and final suffixing completed.")
    return final_features

# --- 3. MAIN PIPELINE FUNCTION ---

def run_resume_pipeline(file_name_without_ext: str, file_type: str):
    """Core function to run the full document parsing and resume feature engineering pipeline."""
    start_time = time()
    
    # 0. Setup and Validation
    input_path = PROJECT_ROOT / "input" / f"{file_name_without_ext}.{file_type}"
    output_name = f"features_{file_name_without_ext}.json"
    output_path = PROJECT_ROOT / "output" / output_name
    
    if not input_path.exists():
        logging.error(f"Error: {input_path} not found. Place file in {PROJECT_ROOT / 'input'}.")
        return

    with open(input_path, "rb") as f:
        binary_data = f.read()

    # 1. Document Parsing (using RAGFlow Parsers)
    print(f"\n--- 1. PARSING {file_type.upper()} File: {input_path.name} ---")
    if file_type == "pdf":
        parser = RAGFlowPdfParser()
        # Minimal options are used for resume text extraction
        filtered_text, tables = parser(binary_data, need_image=False, return_html=False)
    elif file_type == "docx":
        parser = RAGFlowDocxParser()
        secs, tbls = parser(binary_data)
        filtered_text = "\n\n".join([text for text, style in secs if text.strip()])
    else:
        # This branch is technically unreachable due to checks in __main__
        logging.error(f"Unsupported file type: {file_type}.")
        return
        
    elapsed = time() - start_time
    print(f"   Parsing Done in {elapsed:.2f}s. Extracted text length: {len(filtered_text)}")
    
    # 2. Resume Extraction (MOCKED - Converts raw text to structured JSON)
    cv_raw_json = resume_extractor(filtered_text)

    # 3. Resume Feature Engineering Pipeline (init -> step1 -> step2)
    print("\n--- 2. RUNNING RESUME FEATURE PIPELINE ---")
    
    cv_stage1 = refactor_init(cv_raw_json)
    cv_stage2 = refactor_step1(cv_stage1)
    final_features = parse_step2(cv_stage2)

    # 4. Save Final Output
    print(f"\n--- 3. SAVING FINAL FEATURES ---")
    output_path.parent.mkdir(exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(final_features, f, indent=4, ensure_ascii=False)

    total_elapsed = time() - start_time
    print(f"✅ Success! Final features saved to: {output_path}")
    print(f"   Total Pipeline Time: {total_elapsed:.2f}s")
    
# --- 4. EXECUTION ENTRY POINT ---

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python run_pipeline.py <full_file_name_including_extension>")
        print("Example: python run_pipeline.py my_resume.pdf")
        sys.exit(1)
        
    full_file_name = sys.argv[1]
    
    if "." not in full_file_name:
        print("Error: File extension missing. Please specify like 'my_file.pdf'.")
        sys.exit(1)
        
    file_name_without_ext, file_type = full_file_name.rsplit('.', 1)
    file_type = file_type.lower()
    
    if file_type not in ["pdf", "docx"]:
        print(f"Error: Unsupported file type: '{file_type}'. Only 'pdf' and 'docx' are supported.")
        sys.exit(1)
        
    # Run the full pipeline
    run_resume_pipeline(file_name_without_ext, file_type)