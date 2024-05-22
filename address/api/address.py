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

from address.database import Address as AddressDatabase
from address.models import Address as AddressModel

from user.api.authenticate import get_current_user

from passlib.context import CryptContext

from datetime import datetime, timedelta

from typing import List

address_router = APIRouter(
    prefix="/api/v1/address",
    tags=["Address"],
    responses={404: {"description": "Not found"}},
)

@address_router.post("/")
async def create_address(address: AddressModel,
                        user: dict = Depends(get_current_user), 
                        db: Session = Depends(get_db)):
    """
    Manual registration of users on the application
    """
    try:
        address_model = AddressDatabase(**address.model_dump())
        address_model.user_id = user.get("id")

        db.add(address_model)
        db.commit()

        response = {
            'success': True,
            'msg': 'Success.'

        }
        return response
    except Exception as e:
        response = {
            'code': -1,
            'success': False,
            'msg': 'Something went wrong.'

        }
        return response

@address_router.get("/")
async def list(user: dict = Depends(get_current_user), db: Session = Depends(get_db), ):
    """
    Manual registration of users on the application
    """
    try:
        addresses = db.query(AddressDatabase).filter(AddressDatabase.user_id==user.get("id"))
        address_list = [{"street": addr.street, "city": addr.city, "state": addr.state, 
                        "zip_code": addr.zip_code, "country": addr.country,
                        "longitude": addr.longitude, "latitude": addr.latitude, "user_id": addr.user_id} 
                        for addr in addresses]
        response = {
            'code': 1,
            'success': True,
            'msg': 'Success.',
            'data': address_list

        }
        return response
    except Exception as e:
        response = {
            'code': -1,
            'success': False,
            'msg': 'Something went wrong.'

        }
        return response

@address_router.get("/{address_id}")
async def get(address_id: int,
            user: dict = Depends(get_current_user), 
            db: Session = Depends(get_db)):
    """
    Manual registration of users on the application
    """
    try:
        addresses = db.query(AddressDatabase).filter(AddressDatabase.id==address_id, AddressDatabase.user_id==user.get("id")).first()
        response = {
            'code': 1,
            'success': True,
            'msg': 'Success.',
            'data': addresses

        }
        return response
    except Exception as e:
        print(e)
        response = {
            'code': -1,
            'success': False,
            'msg': 'Something went wrong.'

        }
        return response

@address_router.put("/{address_id}")
async def update(address_id: int,
                address: AddressModel,
                user: dict = Depends(get_current_user), 
                db: Session = Depends(get_db)):
    """
    Manual registration of users on the application
    """
    try:
        response = None
        db_address = db.query(AddressDatabase).filter(AddressDatabase.id == address_id, AddressDatabase.user_id==user.get("id")).first()
        
        if db_address:
            for var, value in address.model_dump().items():
                setattr(db_address, var, value) if value else None
            db.commit()
            db.refresh(db_address)
            response = {
                'code': 1,
                'success': True,
                'msg': 'Success.',
                'data': db_address

            }
            return db_address
        return response
    except Exception as e:
        print(e)
        response = {
            'code': -1,
            'success': False,
            'msg': 'Something went wrong.'

        }
        return response

@address_router.delete("/{address_id}")
async def destroy(address_id: int,
                address: AddressModel,
                user: dict = Depends(get_current_user), 
                db: Session = Depends(get_db)):
    """
    Manual registration of users on the application
    """
    response = None
    db_address = db.query(AddressDatabase).filter(AddressDatabase.id == address_id, AddressDatabase.user_id==user.get("id")).first()
    if db_address:
        db.delete(db_address)
        db.commit()
        response = {
            'code': 1,
            'success': True,
            'msg': 'Success.',
            'data': db_address

        }
        return response
    else:
        response = {
            'code': -1,
            'success': False,
            'msg': 'Address does not exist.'

        }
        return response