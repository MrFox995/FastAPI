from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

from app import database

from . import schemas, models

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

# Here what we need to provide are:
#   - Secret Key: it is in our server (hashed)
#   - Algorithm: the algorithm we want use to create Token
#   - Token Expiration Time: how long a user can stay logged in

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire}) # Insert Expiry Time in this format is mandatory if you want use jwt.encode() function
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credendials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        ID: int = payload.get("user_id")

        if ID is None:
            raise credendials_exception
        
        token_data = schemas.TokenData(ID = ID)

    except JWTError:
        raise credendials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)

def get_current_user_v2(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.ID == token.ID).first()

    return user.ID

