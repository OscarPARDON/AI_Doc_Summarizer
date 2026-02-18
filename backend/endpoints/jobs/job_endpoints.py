import sqlite3
from fastapi import APIRouter
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
from services.jobs_manager import get_job
from settings import DBDIR

jobs_router = APIRouter()

@jobs_router.get("/{job_id}")
async def follow_job_status(job_id: str):
    db_cnx = sqlite3.connect(DBDIR)
    db_cnx.row_factory = sqlite3.Row

    job = get_job(db_cnx, uuid=job_id)
    db_cnx.close()

    if job:
        return JSONResponse(status_code=HTTP_200_OK, content={
            "uuid": job["uuid"],
            "status": job["status"],
            "result": job["result"]
        })

    return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"detail": "Job not found"})
