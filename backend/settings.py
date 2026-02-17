import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

WORKDIR = Path(__file__).resolve().parent
DBDIR = WORKDIR / "db" / "jobs_list.db"
APIKEY = os.getenv("APIKEY")
TEMP_FILE_STORAGE_DIR = os.getenv("TEMP_FILE_STORAGE_DIR", "/tmp/files")

SUPPORTED_DOCTYPES_MIME = [
    "text/plain",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/html",
    "message/rfc822",
    "application/vnd.ms-outlook"
]