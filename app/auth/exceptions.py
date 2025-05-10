from fastapi import status, HTTPException

from app.exceptions import BaseAppException


class UserExistException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=409)


class UserNotExistException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=401)


class IncorrectCredentialsException(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=401)


UserCredentialsException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )