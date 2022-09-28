from typing import Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fin_app_dataset.db import init_db

from .routers import company, stockprice, financial, sector, news
from .dependencies.auth import get_current_user
from .settings import settings


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if settings.DISABLE_AUTH:
    async def disable_auth_dep(ppp: Optional[int] = None):
        return ppp
    app.dependency_overrides[get_current_user] = disable_auth_dep

app.include_router(stockprice.router)
app.include_router(financial.router)
app.include_router(company.router)
app.include_router(sector.router)
app.include_router(news.router)

# init_db(recreate_database=False)
