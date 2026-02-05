from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import PyPDF2
import io
import easyocr
from pdf2image import convert_from_bytes
import numpy as np


def ocr_pdf(pdf_bytes: bytes) -> str:
    """Run OCR on scanned PDF"""
    reader = easyocr.Reader(['en'], gpu=False)
    images = convert_from_bytes(pdf_bytes)

    ocr_text = ""
    for img in images:
        result = reader.readtext(np.array(img), detail=0)
        ocr_text += " ".join(result) + "\n"

    return ocr_text


def extract_and_chunk_pdf(file) -> List[Document]:
    pdf_bytes = file.file.read()
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

    full_text = ""

    # 1️⃣ Try normal extraction
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    # 2️⃣ If no text → OCR fallback
    if not full_text.strip():
        print("⚠️ No text found, running OCR...")
        full_text = ocr_pdf(pdf_bytes)

    if not full_text.strip():
        return []

    # 3️⃣ Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = splitter.split_text(full_text)

    # 4️⃣ Convert to LangChain Documents
    documents = [Document(page_content=chunk) for chunk in chunks]

    return documents
