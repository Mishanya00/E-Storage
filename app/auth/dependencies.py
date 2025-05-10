from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from app.auth.service import decode_access_token, decode_refresh_token
from app.auth.schemas import UserSchema
from app.repository.queries import get_user_by_email
from app.auth.exceptions import UserCredentialsException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        email = payload.get("sub")
        if email is None:
            raise UserCredentialsException
        user = await get_user_by_email(email)
        if user is None:
            raise UserCredentialsException
        return UserSchema(**user)
    except ExpiredSignatureError:
        try:
            payload = decode_refresh_token(token)
            pass
        except InvalidTokenError:
            raise UserCredentialsException
    except InvalidTokenError:
        raise UserCredentialsException