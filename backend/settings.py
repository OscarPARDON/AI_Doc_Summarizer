import os

from dotenv import load_dotenv

load_dotenv()

TEMP_FILE_STORAGE_DIR = os.getenv("TEMP_FILE_STORAGE_DIR", "../temp_file_storage/")
