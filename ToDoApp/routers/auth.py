from fastapi import APIRouter

router = APIRouter()


@router.get("/auth/")
async def user():
    return {"user": "User Authenticated"}
