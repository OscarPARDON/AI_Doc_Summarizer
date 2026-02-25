import os
from enum import IntFlag
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

WORKDIR = Path(__file__).resolve().parent
DBDIR = WORKDIR / "db" / "jobs_list.db"
TEMP_FILE_STORAGE_DIR = "/tmp/files"
MAX_FILE_SIZE = 128_000_000 # 128 Mo

class STATUS_CODES(IntFlag):
    Pending = 1
    Success = 2
    Failure = 3

APIKEY = os.getenv("APIKEY","AIzaSyBztk6dYHbqiHg4Aah_wOc7oWand7WMRpY")
MODEL_PROMPT = """Tu ne vas recevoir que le contenu de fichiers.
Tu DOIS répondre UNIQUEMENT avec du JSON valide.
Ne mets PAS de ```json.
Ne mets PAS de texte avant ou après.
Format EXACT attendu :
{
  "titre": "...",
  "resume": "...",
  "mots_cles": ["..."],
  "type_document": "...",
  "langue": "..."
}"""

SUPPORTED_DOCTYPES_MIME = [
    "text/plain",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/html",
    "message/rfc822",
    "application/vnd.ms-outlook"
]

LOG_LEVEL = "INFO"