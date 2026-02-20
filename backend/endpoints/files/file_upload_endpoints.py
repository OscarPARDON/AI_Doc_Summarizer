from services.files_treatment_service import on_upload_complete
from tuspyserver import create_tus_router
from services.upload_validation import validate_upload
from settings import TEMP_FILE_STORAGE_DIR, MAX_FILE_SIZE

# Create a router to receive files using TUS
tus_router = create_tus_router(
    files_dir=TEMP_FILE_STORAGE_DIR, # path to store the received file
    max_size=MAX_FILE_SIZE, # max size of the received file
    days_to_keep=1, # retention period to keep a partially uploaded file
    pre_create_hook=validate_upload, # Pre-upload validation
    on_upload_complete= on_upload_complete # function triggered when the upload is completed
)
