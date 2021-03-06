from fastapi import APIRouter
from shop_list.api.api_v1.endpoints import login, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
