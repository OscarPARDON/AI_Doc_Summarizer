from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_413_CONTENT_TOO_LARGE
from settings import SUPPORTED_DOCTYPES_MIME


def validate_upload(metadata: dict, upload_info: dict):
    """ Validate the received file """

    # require filename in metadata
    if "filename" not in metadata:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Filetype is required in metadata")

    # Check file size limits
    if upload_info["size"] and upload_info["size"] > 1_000_000_000:  # 1 GB
        raise HTTPException(status_code=HTTP_413_CONTENT_TOO_LARGE, detail="Filesize is over 1GB")

    # Validate filetype
    if "filetype" in metadata:
        if metadata["filetype"] not in SUPPORTED_DOCTYPES_MIME:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Filetype is not supported")
    else :
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Filetype is required in metadata")