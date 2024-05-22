from fastapi import APIRouter
from address.api.address import address_router 

address_api_router = APIRouter()
address_api_router.include_router(address_router)