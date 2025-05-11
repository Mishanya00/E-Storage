import hashlib
import re
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException, status
from psycopg.errors import UniqueViolation
import jwt

from app.config import ALGORITHM, REFRESH_JWT_SECRET, ACCESS_JWT_SECRET, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from app.auth.exceptions import UserExistException, UserNotExistException, IncorrectCredentialsException
from app.repository import queries
from app.auth.schemas import UserSchema, UserFormSchema
from app.storage.service import create_email_folder


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
        create_email_folder(user.email)     # Maybe I should use BackgroundTasks
        return True
    except UniqueViolation as e:
        raise UserExistException('User already exists') from e


async def authenticate_user(email: str, password: str) -> UserSchema | None:
    # user_data = await queries.get_user_by_email(email)
    user = await get_user(email)
    if not user:
        raise UserNotExistException('User does not exist')
    if not verify_password(password, user.hashed_pswd):
        raise IncorrectCredentialsException('Incorrect password')
    return user


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


def create_jwt(data: dict, expires_delta: timedelta, secret: str) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return dict(jwt.decode(token, ACCESS_JWT_SECRET, algorithms=[ALGORITHM]))


def decode_refresh_token(token: str) -> dict:
    return dict(jwt.decode(token, REFRESH_JWT_SECRET, algorithms=[ALGORITHM]))


def create_access_token(data: dict) -> str:
    return create_jwt(data, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), ACCESS_JWT_SECRET)


def create_refresh_token(data: dict) -> str:
    return create_jwt(data, timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES), REFRESH_JWT_SECRET)