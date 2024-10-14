from fastapi import APIRouter, status, Depends
from starlette.responses import Response

from schemas.auth import LoginSchema, SuccessLoginSchema
from services.auth import AuthService


router = APIRouter(prefix="/auth", tags=["Войти"])


@router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=SuccessLoginSchema,
)
async def create_auth_session(
    data: LoginSchema,
    auth_service: AuthService = Depends(),
) -> Response:
    return await auth_service.create_token(data=data)
