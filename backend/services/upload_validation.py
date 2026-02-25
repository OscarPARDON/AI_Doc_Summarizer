import logging
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_413_CONTENT_TOO_LARGE
from settings import SUPPORTED_DOCTYPES_MIME

logger = logging.getLogger(__name__)

def validate_upload(metadata: dict, upload_info: dict):
    """ Validate the received file """

    # require filename in metadata
    if "filename" not in metadata:
        logger.warning("File refused : No filename in file metadata")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Filetype is required in metadata")

    # Check file size limits
    if upload_info["size"] and upload_info["size"] > 1_000_000_000:  # 1 GB
        logger.warning("File refused : size too large")
        raise HTTPException(status_code=HTTP_413_CONTENT_TOO_LARGE, detail="Filesize is over 1GB")

    # Validate filetype
    if "filetype" in metadata:
        if metadata["filetype"] not in SUPPORTED_DOCTYPES_MIME:
            logger.warning("File refused : Unsupported filetype")
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Filetype is not supported")
    else :
        logger.warning("File refused : No filetype in file metadata")
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Filetype is required in metadata")