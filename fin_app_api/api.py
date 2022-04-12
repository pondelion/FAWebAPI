from typing import Optional

from fastapi import FastAPI

from .routers import stock
from .dependencies.auth import get_current_user
from .settings import settings


app = FastAPI()

if settings.DISABLE_AUTH:
    async def disable_auth_dep(ppp: Optional[int] = None):
        return ppp
    app.dependency_overrides[get_current_user] = disable_auth_dep

app.include_router(stock.router)
