from fastapi import FastAPI
from fastapi_pagination import add_pagination
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from api.router import api_router
from core.config import settings

app = FastAPI(
    title="Online Store",
    openapi_url="/api/openapi.json",
    docs_url="/api/swagger",
)

add_pagination(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings().cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

app.add_middleware(SessionMiddleware, secret_key=settings().SESSION_MIDDLEWARE_SECRET)
