from fastapi import APIRouter

test_router = APIRouter()

@test_router.get("/cnx_test")
async def test_connexion():
    return {"status":200,"message": "Connexion Successful"}