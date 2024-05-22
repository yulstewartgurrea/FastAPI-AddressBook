from fastapi import APIRouter
from user.api.register import register_user_router 
from user.api.authenticate import authenticate_user_router 

user_api_router = APIRouter()
user_api_router.include_router(register_user_router)
user_api_router.include_router(authenticate_user_router)