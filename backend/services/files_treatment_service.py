import json
import os
from services.files_content_scrapper import scrap_content_from_file
import sqlite3
from services.files_content_summarizer import summarize_with_ai
from services.jobs_manager import init_job, update_job, delete_job
import asyncio

from settings import DBDIR


async def trigger_scrapper_and_summarizer(file_path: str):
    # Job list initialization
    db_cnx = sqlite3.connect(DBDIR,check_same_thread=False)

    # Job initialization
    file_uuid = os.path.basename(file_path)
    init_job(db_cnx, uuid = file_uuid, status = "En cours de traitement : Récupération du contenu du fichier")

    # File content scrapping
    file_content = scrap_content_from_file(file_path)
    if file_content:
        update_job(db_cnx, uuid = file_uuid, status= "En cours de traitement : Le contenu du fichier est en train d'être résumé", result="")

        response = await summarize_with_ai(file_content)

        if response:
            update_job(db_cnx, uuid = file_uuid, status= "Traitement terminé : Le contenu est disponible", result=json.dumps(response, ensure_ascii=False) )
        else :
            update_job(db_cnx, uuid = file_uuid, status= "Traitement terminé : Echec du traitement", result="")
    else :
        update_job(db_cnx, uuid=file_uuid, status="Traitement terminé : Le type de fichier n'est pas supporté", result="")

    os.remove(file_path)
    db_cnx.close()


def on_upload_complete(file_path, metadata):
    asyncio.get_event_loop().call_soon_threadsafe(
        lambda: asyncio.create_task(trigger_scrapper_and_summarizer(file_path))
    )
