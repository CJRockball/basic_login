import datetime as dt
from typing import Dict

from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt
from passlib.handlers.sha2_crypt import sha512_crypt as crypto

from utils.schemas import User
from utils.db_util import get_user 
from utils.security import OAuth2PasswordBearerWithCookie

import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
COOKIE_NAME = os.getenv('COOKIE_NAME')

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl='token')

def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = dt.datetime.utcnow() + dt.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt


def authenticate_user(username: str, plain_password: str) -> User:
    user = get_user(username)
    if not user:
        return False
    if not crypto.verify(plain_password, user.hashed_password):
        return False
    return user


def decode_token(token: str) -> User:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED, 
        detail='Could not validate credentials'
    )
    token = token.removeprefix('Bearer').strip()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('username')
        if username is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    user = get_user(username)
    return user


def get_current_user_from_token(token:str = Depends(oauth2_scheme)) -> User:
    user = decode_token(token)
    return user

def get_current_user_from_cookie(request:Request) -> User:
    token = request.cookies.get(COOKIE_NAME)
    user = decode_token(token)
    return user