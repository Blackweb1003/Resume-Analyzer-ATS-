import fitz


def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        document = fitz.open(stream=file_bytes, filetype="pdf")
    except Exception as exc:
        raise ValueError("Invalid or corrupted PDF file.") from exc

    pages: list[str] = []

    try:
        for page in document:
            pages.append(page.get_text("text"))
    finally:
        document.close()

    return "\n".join(pages).strip()
