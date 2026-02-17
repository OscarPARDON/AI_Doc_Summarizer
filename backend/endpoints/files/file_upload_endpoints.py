from services.files_upload_services import log_upload
from tuspyserver import create_tus_router

tus_router = create_tus_router(
    files_dir="/tmp/files", # path to store files
    max_size=128_000_000, # max upload size in bytes (128mo)
    days_to_keep=1, # retention period
    on_upload_complete= log_upload # function triggered when the upload is completed
)
