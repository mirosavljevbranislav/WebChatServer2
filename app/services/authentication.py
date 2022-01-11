from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse

from jose import jwt, JWTError
from starlette.status import HTTP_404_NOT_FOUND, HTTP_401_UNAUTHORIZED

from app.services import user
from app.model.token import TokenData

from passlib.context import CryptContext

SECRET_KEY = "6ad9e80da5855267057ac983fce2ee1ea067b39e6bb478bc61eac514b4c38aa4"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    """
    Check password hash
    :param plain_password: plain password
    :param hashed_password: hashed password
    :return:
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Return hashed password
    :param password: password to hash
    :return:
    """
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str):
    user_for_auth = user.get_user(username=username)
    if not user_for_auth:
        return JSONResponse(status_code=HTTP_404_NOT_FOUND, content={"Message": "User not found"})
    if not verify_password(password, user_for_auth["password"]):
        return JSONResponse(status_code=HTTP_401_UNAUTHORIZED, content={"Message": "Incorrect username or password"})
    return user_for_auth


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    current_user = user.get_user(username=token_data.username)
    if current_user is None:
        raise credentials_exception
    return current_user
