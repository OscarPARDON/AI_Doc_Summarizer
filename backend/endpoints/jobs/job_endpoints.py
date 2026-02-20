import sqlite3
from fastapi import APIRouter
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from services.jobs_manager import get_job
from settings import DBDIR

jobs_router = APIRouter()

@jobs_router.get("/{job_id}")
async def follow_job_status(job_id: str)->JSONResponse:
    """This endpoint allow to follow the state of a job with its uuid"""

    # DB connexion
    db_cnx = sqlite3.connect(database=DBDIR)
    db_cnx.row_factory = sqlite3.Row

    # Fetching the job from the database and close the connexion
    job = get_job(cnx=db_cnx, uuid=job_id)
    db_cnx.close()

    # If the job is found, return its state
    if job:
        return JSONResponse(status_code=HTTP_200_OK, content={
            "uuid": job["uuid"],
            "filename": job["filename"],
            "status": job["status"],
            "result": job["result"]
        })
    # If no job with this UUID is found, return a 404 not found
    return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": "Job not found"})
