import json
import os
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK
from services.files_content_scrapper import scrap_content_from_file
import sqlite3
from services.files_content_summarizer import summarize_with_ai
from services.jobs_manager import init_job, update_job
import asyncio
from settings import DBDIR, STATUS_CODES


async def trigger_scrapper_and_summarizer(file_path: str, metadata: dict):
    """ This function manage the treatment of the file (scrapping, summarizing and job update)"""

    # DB connexion
    db_cnx = sqlite3.connect(database=DBDIR,check_same_thread=False)

    # file UUID extraction
    file_uuid = os.path.basename(file_path)
    filename = metadata["filename"]

    # Initialization of the job
    init_job(db_cnx, uuid = file_uuid, filename=filename, status_code = STATUS_CODES.Pending, message = "Récupération du contenu du fichier")

    # File content scrapping
    file_content = scrap_content_from_file(file_path)
    if file_content:

        # Update the job
        update_job(db_cnx, uuid = file_uuid, status_code=STATUS_CODES.Pending, message= "Le contenu du fichier est en train d'être résumé", result="")

        # File summarizing
        summary = await summarize_with_ai(file_content)

        if summary:
            update_job(db_cnx, uuid = file_uuid, status_code=STATUS_CODES.Success, message= "Le contenu est disponible", result=json.dumps(summary, ensure_ascii=False) )
        else :
            update_job(db_cnx, uuid = file_uuid, status_code=STATUS_CODES.Failure, message= "Le fichier n'a pas pu être resumé", result="")
    else :
        update_job(db_cnx, uuid=file_uuid, status_code=STATUS_CODES.Failure, message="Le contenu n'a pas pu être extrait", result="")

    # File suppression
    os.remove(file_path)
    # Close the connexion to the db
    db_cnx.close()


def on_upload_complete(file_path: str, metadata : dict) -> JSONResponse :
    """ Start the asynchronous treatment of the file, confirm the end of the file upload"""

    asyncio.get_event_loop().call_soon_threadsafe(
        lambda: asyncio.create_task(trigger_scrapper_and_summarizer(file_path=file_path, metadata=metadata))
    )
    return JSONResponse(status_code=HTTP_200_OK, content={"message": "File successfully uploaded"})
