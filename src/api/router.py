from fastapi import APIRouter
from api.v1.good_group import router as good_group_router
from api.v1.good import router as good_router
from api.v1.specification import router as specification_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(good_group_router)
v1_router.include_router(good_router)
v1_router.include_router(specification_router)

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
