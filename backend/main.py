import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from endpoints.test.test_endpoints import test_router

router_values = APIRouter()
app = FastAPI(title="AI_doc_summarizer")

app.include_router(test_router,prefix="/test", tags=["Connexion Test"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #allow_origins=["http://localhost:8080"],
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)