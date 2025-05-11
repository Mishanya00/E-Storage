from typing import Annotated

from pydantic import BaseModel, Field


EMAIL_PATTERN = r"\b[\w\-\.]+@(?:[\w-]+\.)+[\w\-]{2,4}\b"


class UserFormSchema(BaseModel):
    email: Annotated[str, Field(max_length=64, pattern=EMAIL_PATTERN)]
    password: Annotated[str, Field(min_length=8)]


class UserSchema(BaseModel):
    user_id: Annotated[int, Field(ge=0)]
    email: str
    hashed_pswd: Annotated[str, Field(exclude=True)]


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
