import io
import sys
import threading

import pdfplumber
from PIL import Image

from .ocr import OCR
from .recognizer import Recognizer
from .layout_recognizer import AscendLayoutRecognizer
from .layout_recognizer import LayoutRecognizer4YOLOv10 as LayoutRecognizer
from .table_structure_recognizer import TableStructureRecognizer

# Global lock to keep pdfplumber thread-safe
LOCK_KEY_pdfplumber = "global_shared_lock_pdfplumber"
if LOCK_KEY_pdfplumber not in sys.modules:
    sys.modules[LOCK_KEY_pdfplumber] = threading.Lock()


def init_in_out(args):
    """
    Initialize input images and output filenames.

    Args:
        args.inputs: Path to file or directory.
        args.output_dir: Where output images will be saved.

    Returns:
        images: List[PIL.Image]
        outputs: List[str]
    """

    import os
    import traceback
    from common.file_utils import traversal_files

    images = []
    outputs = []

    # Ensure output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    # -----------------------------------------
    # Handle PDF pages using pdfplumber
    # -----------------------------------------
    def pdf_pages(fnm, zoomin=3):
        nonlocal outputs, images
        with sys.modules[LOCK_KEY_pdfplumber]:
            pdf = pdfplumber.open(fnm)
            images = [
                page.to_image(resolution=72 * zoomin).annotated
                for _, page in enumerate(pdf.pages)
            ]
        for i in range(len(images)):
            base_name = os.path.basename(fnm)
            outputs.append(f"{base_name}_{i}.jpg")
        pdf.close()

    # -----------------------------------------
    # Handle image file (jpg/png/etc.)
    # -----------------------------------------
    def images_and_outputs(fnm):
        nonlocal outputs, images
        if fnm.lower().endswith(".pdf"):
            pdf_pages(fnm)
            return
        try:
            with open(fnm, "rb") as fp:
                binary = fp.read()
            images.append(Image.open(io.BytesIO(binary)).convert("RGB"))
            outputs.append(os.path.basename(fnm))
        except Exception:
            traceback.print_exc()

    # -----------------------------------------
    # Process directory or a single file
    # -----------------------------------------
    if os.path.isdir(args.inputs):
        for fnm in traversal_files(args.inputs):
            images_and_outputs(fnm)
    else:
        images_and_outputs(args.inputs)

    # Prepend output directory
    outputs = [os.path.join(args.output_dir, o) for o in outputs]

    return images, outputs


__all__ = [
    "OCR",
    "Recognizer",
    "LayoutRecognizer",
    "AscendLayoutRecognizer",
    "TableStructureRecognizer",
    "init_in_out",
]
