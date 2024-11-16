from fastapi import APIRouter, status, Depends, Request

from schemas.outlet import OutletSchema
from services.outlet import OutletService

router = APIRouter(prefix="/outlets", tags=["Торговый точки"])


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=list[OutletSchema],
)
async def create_auth_session(
    request: Request,
    outlet_service: OutletService = Depends(),
) -> list[OutletSchema]:
    return await outlet_service.get_by_token(token=request.cookies.get("token"))
