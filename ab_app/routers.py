from fastapi import APIRouter
from user.routes import user_api_router
from address.routes import address_api_router

router = APIRouter()
router.include_router(user_api_router)
router.include_router(address_api_router)
