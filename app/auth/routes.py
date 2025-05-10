from typing import Annotated

from fastapi import APIRouter, HTTPException, Body

from app.auth import service
from app.auth.schemas import UserFormSchema
from app.exceptions import BaseAppException


auth_router = APIRouter()


@auth_router.post("/register")
async def register_user(user: Annotated[UserFormSchema, Body()]):
    try:
        await service.register_user(user)
        return {'message': 'user is registered!'}
    except BaseAppException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))