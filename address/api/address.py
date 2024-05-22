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

from geopy.distance import geodesic


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
    Create addresses
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
    List all addresses of the user
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
    Get a specific address using the id
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
    Updates an address
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
    Deletes an address
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
    
@address_router.get("/search/coordinates")
async def search_by_coordinates(
    longitude: float = Query(..., description="Longitude of the search center"),
    latitude: float = Query(..., description="Latitude of the search center"),
    user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Get specific address using coordinates
    """
    try:
        addresses = db.query(AddressDatabase).filter(
            AddressDatabase.user_id==user.get("id"),
            AddressDatabase.longitude==longitude,
            AddressDatabase.latitude==latitude
        )
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
    
@address_router.get("/search/nearby")
async def search_nearby(
    current_longitude: float = Query(..., description="Longitude of the search center"),
    current_latitude: float = Query(..., description="Latitude of the search center"),
    max_distance: float = Query(default=5, description="Maximum distance from the point in miles"),
    user: dict = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Get specific address using coordinates
    """
    try:
        nearby_addresses = []
        addresses = db.query(AddressDatabase).filter(
            AddressDatabase.user_id==user.get("id")
        )
        for address in addresses:
            # Check for valid coordinates in the database entries
            if (address.latitude and address.longitude and 
                not (address.latitude == current_latitude and address.longitude == current_longitude)):
                address_coords = (address.latitude, address.longitude)
                current_coords = (current_latitude, current_longitude)
                distance = geodesic(address_coords, current_coords).miles
                if distance <= int(max_distance):
                    nearby_addresses.append(address)
                    
        response = {
            'code': 1,
            'success': True,
            'msg': 'Success.',
            'data': nearby_addresses

        }
        return response
    except Exception as e:
        response = {
            'code': -1,
            'success': False,
            'msg': 'Something went wrong.'

        }
        return response