from datetime import date as datetime_date
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import CognitoClaims

from fin_app_dataset.services.local_transfered_cache.rdynamo_to_lrdb.news import (
    GoogleNewsService,
)

from ..dependencies.auth import get_current_user
from ..utils.time_record import time_record


router = APIRouter(
    prefix='/news',
    tags=['News API'],
)

google_news_svc = GoogleNewsService()


@router.get('/daily')
async def get_by_date(
    date: datetime_date,
    current_user: CognitoClaims = Depends(get_current_user),
):
    news = [d.__dict__ for d in google_news_svc.get_by_date(date)]
    return {'news_list': news}
