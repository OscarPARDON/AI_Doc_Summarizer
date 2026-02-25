import logging
import os
import re
import extract_msg
import magic
from typing import Union
from pypdf import PdfReader
from docx import Document
from bs4 import BeautifulSoup
import email
from settings import SUPPORTED_DOCTYPES_MIME

logger = logging.getLogger(__name__)

def detect_file_type(file_path: str) -> Union[str, bool]:
    """
    Detect and return mime type of file, return the filetype if it is in the list of supported types, return false if unsupported.
    """

    # Extract the MIME from the file
    mime = magic.Magic(mime=True)
    file_mime = mime.from_file(file_path)

    # Clean the MIME to only get the type
    file_mime = file_mime.split(";")[0].strip()

    if file_mime in SUPPORTED_DOCTYPES_MIME :
        return file_mime

    logger.warning(msg=f"{os.path.basename(file_path)} : Unsupported filetype")
    return False


def extract_txt(file_path: str) -> str:
    """ Extract the content from a .txt file """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def extract_pdf(file_path: str) -> str:
    """ Extract the content from a .pdf file """

    # Open the file and extract the content
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    # Clean the extracted content from unnecessary spaces and blanks
    text = text.strip()
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)

    return text


def extract_docx(file_path: str) -> str:
    """Extract the content from a .docx file """
    doc = Document(file_path)
    return "\n".join(para.text for para in doc.paragraphs)


def extract_html(file_path: str) -> str:
    """ Extract the content from a .html file """

    with open(file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    text = soup.get_text(separator="\n")
    text = text.strip()
    text = re.sub(r'\n\s*\n+', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    return text


def extract_eml(file_path: str) -> str:
    """Extract the content from a .eml file (email)"""

    # Open the file
    with open(file_path, "r", encoding="utf-8") as f:
        msg = email.message_from_file(f)

    # Extract the content
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload:
                    return payload.decode(errors="ignore")
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            return payload.decode(errors="ignore")

    return ""


def extract_msg_file(file_path: str) -> str:
    """Extract content from a .msg file (email)"""
    msg = extract_msg.Message(file_path)
    return msg.body or ""

def scrap_content_from_file(file_path:str) -> Union[str, bool]:
    """Return the content of a file using the adapted scrapper based on its detected type"""

    detected_mime = detect_file_type(file_path)

    if detected_mime:
        file_content = ""
        match detected_mime:
            case "text/plain":
                file_content = extract_txt(file_path)
            case "application/pdf":
                file_content = extract_pdf(file_path)
            case "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                file_content = extract_docx(file_path)
            case "text/html":
                file_content = extract_html(file_path)
            case "message/rfc822" :
                file_content = extract_eml(file_path)
            case "application/vnd.ms-outlook":
                file_content = extract_msg_file(file_path)

        return file_content

    return False