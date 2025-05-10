import hashlib
import re

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation

from app.auth.exceptions import UserExistException, UserNotExistException
from app.repository import queries
from app.auth.schemas import UserSchema, UserFormSchema


EMAIL_PATTERN = r"\b[\w\-\.]+@(?:[\w-]+\.)+[\w\-]{2,4}\b"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password:
        return True
    return False


def validate_email(email: str) -> str:
    if not re.fullmatch(EMAIL_PATTERN, email):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid email format")
    return email


async def register_user(user: UserFormSchema):
    hashed_password = hashlib.sha256(user.password.encode()).hexdigest()
    try:
        await queries.create_user(user.email, hashed_password)
        return True
    except UniqueViolation as e:
        raise UserExistException('User already exists') from e


async def is_user_exist(email: str) -> bool:
    user_data = await queries.get_user_by_email(email)
    if user_data:
        return True
    return False


async def get_user(email: str) -> UserSchema | None:
    user_data = await queries.get_user_by_email(email)
    if user_data is None:
        raise UserNotExistException('User does not exist')
    return UserSchema(**user_data)