from fastapi import Depends

from core.exceptions import (
    invalid_creds_exception,
)
from db.repositories.auth import OutletRedisRepository
from schemas.outlet import OutletSchema


class OutletService:
    def __init__(
        self,
        outlet_repository: OutletRedisRepository = Depends(),
    ):
        self._outlet_repository = outlet_repository

    async def get_by_token(self, token: str | None) -> list[OutletSchema]:
        outlets = await self._outlet_repository.get_list(token=token)

        if outlets is None:
            raise invalid_creds_exception

        return outlets
