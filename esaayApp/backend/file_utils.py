import PyPDF2
import docx
import tempfile
import os

def extract_text_from_pdf(file_path):
    """
    Extracts all text from a PDF file.
    :param file_path: Path to the PDF file.
    :return: Extracted text as a string.
    """
    text = ""
    with open(file_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text


def extract_text_from_docx(file_path):
    """
    Extracts all text from a DOCX file.
    :param file_path: Path to the DOCX file.
    :return: Extracted text as a string.
    """
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text