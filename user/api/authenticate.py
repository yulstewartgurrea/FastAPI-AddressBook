from fastapi import (
    APIRouter,
    Query,
    Depends
)
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from sqlalchemy.orm import Session

from typing import Optional

from ab_app.database import get_db
from ab_app.settings import (
    ALGORITHM,
    SECRET_KEY
)

from user.database import User as UserDatabase
from user.models import User as UserModel

from passlib.context import CryptContext

from datetime import datetime, timedelta

from jose import jwt, JWTError

authenticate_user_router = APIRouter(
    prefix="/api/v1/authenticate",
    tags=["Authenticate"],
    responses={404: {"description": "Not found"}},
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    test = bcrypt_context.verify(plain_password, hashed_password)
    return test

async def authenticate_user(username: str, password: str, db):
    """
    Manual registration of users on the application
    """
    print(username, password)
    user = db.query(UserDatabase).filter(UserDatabase.username==username).first()
    
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

async def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + expires_delta(hours=24)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")

        if username is None or user_id is None:
            raise HTTPException(status_code=404, detail="User not found")
        return {"username": username, "id": user_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="User not found")
    
@authenticate_user_router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends((get_db))):
    user = await authenticate_user(form_data.username, form_data.password, db)
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token_expires = timedelta(minutes=60)
    token = await create_access_token(
        user.username,
        user.id,
        expires_delta=token_expires
    )
    response = {
        'msg': 'Success',
        'success': True,
        'data': {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "token": token
        }
    }
    return response