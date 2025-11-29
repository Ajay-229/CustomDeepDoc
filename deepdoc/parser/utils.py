from rag.nlp import find_codec


def get_text(fnm: str, binary=None) -> str:
    txt = ""
    if binary:
        # This block correctly uses find_codec for binary data
        encoding = find_codec(binary)
        txt = binary.decode(encoding, errors="ignore")
    else:
        # FIX: Explicitly use UTF-8 encoding to prevent UnicodeDecodeError (e.g., charmap codec error)
        with open(fnm, "r", encoding="utf-8") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                txt += line
    return txt