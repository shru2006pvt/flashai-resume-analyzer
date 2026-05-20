import os
import pdfplumber
from docx import Document
from analyzer.utils import clean_text


def extract_text_from_pdf(file_path):
    if not os.path.exists(file_path):
        return ""
    text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return clean_text("\n\n".join(text))


def extract_text_from_docx(file_path):
    if not os.path.exists(file_path):
        return ""
    document = Document(file_path)
    lines = []
    for paragraph in document.paragraphs:
        if paragraph.text:
            lines.append(paragraph.text)
    return clean_text("\n".join(lines))


def extract_text_from_txt(file_path):
    if not os.path.exists(file_path):
        return ""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as handle:
        text = handle.read()
    return clean_text(text)


def parse_resume(file_path):
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()
    if extension == ".pdf":
        return extract_text_from_pdf(file_path)
    if extension == ".docx":
        return extract_text_from_docx(file_path)
    if extension == ".txt":
        return extract_text_from_txt(file_path)

    raise ValueError("Unsupported resume format. Upload PDF, DOCX, or TXT.")


def parse_job_description(text=None, file_path=None):
    if file_path:
        _, extension = os.path.splitext(file_path)
        extension = extension.lower()
        if extension == ".pdf":
            return extract_text_from_pdf(file_path)
        if extension == ".docx":
            return extract_text_from_docx(file_path)
        if extension == ".txt":
            return extract_text_from_txt(file_path)
        raise ValueError("Unsupported JD format. Use PDF, DOCX, or TXT.")

    if text is None:
        return ""
    return clean_text(text)
