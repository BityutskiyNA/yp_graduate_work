from fastapi import Depends, HTTPException, status

from config import config
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from typing import Annotated
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = config.jwt.secret_key
ALGORITHM = "HS256"


async def get_user_id_from_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return user_id
