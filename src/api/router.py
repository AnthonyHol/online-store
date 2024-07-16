from fastapi import APIRouter
from api.v1.lc.good_group import router as good_group_router
from api.v1.lc.good import router as good_router
from api.v1.lc.specification import router as specification_router


lc_router = APIRouter(prefix="/1c")
lc_router.include_router(good_group_router)
lc_router.include_router(good_router)
lc_router.include_router(specification_router)

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(lc_router)

api_router = APIRouter(prefix="/api")
api_router.include_router(v1_router)
