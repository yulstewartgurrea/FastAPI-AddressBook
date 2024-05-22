from fastapi import (
    APIRouter,
    Query,
    Depends
)
from fastapi.exceptions import HTTPException

from sqlalchemy.orm import Session

from ab_app.database import get_db

from user.database import User as UserDatabase
from user.models import User as UserModel

from passlib.context import CryptContext

import logging

register_user_router = APIRouter(
    prefix="/api/v1/register",
    tags=["Register"],
    responses={404: {"description": "Not found"}},
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return bcrypt_context.hash(password)

@register_user_router.post("/")
async def create_user(user: UserModel, db: Session = Depends(get_db)):
    """
    Manual registration of users on the application
    """
    user_model = UserDatabase()
    user_model.email = user.email
    user_model.username = user_model.email

    hashed_password = get_password_hash(user.password)
    user_model.password = hashed_password

    db.add(user_model)
    db.commit()

    response = {
        'success': True,
        'msg': 'Success.'

    }
    return response