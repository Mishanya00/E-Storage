from typing import Annotated

from fastapi import APIRouter

from app.config import ACCESS_JWT_SECRET


auth_router = APIRouter()


@auth_router.get("/register")
async def get_register_user():
    return {"message": "in development"}