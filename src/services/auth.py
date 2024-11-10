import json
from json import JSONDecodeError

import aiohttp
from itsdangerous import URLSafeTimedSerializer
from loguru import logger
from pydantic import ValidationError
from starlette.responses import JSONResponse, Response

from core.config import settings
from core.exceptions import (
    invalid_creds_exception,
    outlets_validate_exception,
    outlets_json_decode_exception,
    outlets_1c_error_exception,
)
from schemas.auth import LoginSchema, SuccessLoginSchema, OutletSchema


class AuthService:
    async def create_token(self, data: LoginSchema) -> Response:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                settings().auth_login_1c_url, json=data.model_dump()
            ) as response:
                response_data = await response.text()
                print(f"{data.model_dump_json()=}")
                print(f"{response_data=}")

                if "403" in response_data:
                    logger.error(f"{invalid_creds_exception.detail}")
                    raise invalid_creds_exception
                elif "[" and "]" in response_data:
                    serializer = URLSafeTimedSerializer(settings().AUTH_SECRET)
                    token = serializer.dumps(data.login, salt="session")

                    try:
                        data_list = json.loads(response_data)
                        outlets = [OutletSchema(**item) for item in data_list]
                    except JSONDecodeError:
                        raise outlets_json_decode_exception
                    except ValidationError:
                        raise outlets_validate_exception

                    result = SuccessLoginSchema(login=data.login, outlets=outlets)
                    response = JSONResponse(content=result.dict())
                    response.set_cookie(key="token", value=token, httponly=True)

                    return response
                else:
                    raise outlets_1c_error_exception
