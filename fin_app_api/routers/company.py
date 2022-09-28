from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import CognitoClaims

from fin_app_dataset.services.local_transfered_cache.rs3_to_lrdb.stock import (
    CompanyService,
)

from ..dependencies.auth import get_current_user
from ..utils.time_record import time_record


router = APIRouter(
    prefix='/company',
    tags=['Company API'],
)

company_svc = CompanyService()


@router.get('/')
async def get_companies(
    current_user: CognitoClaims = Depends(get_current_user),
):
    @time_record
    def _get_companies():
        records = company_svc.get_all()
        companies = [d.__dict__ for d in records]
        [c.update({'sector_name': r.sector.name}) for c, r in zip(companies, records)]
        return companies
    return {'company_list': _get_companies()}


@router.get('/{code}')
async def get_company(
    code: int,
    current_user: CognitoClaims = Depends(get_current_user),
):
    @time_record
    def _get_companies():
        records = company_svc.get_by_code(code=code)
        companies = [d.__dict__ for d in records]
        [c.update({'sector_name': r.sector.name}) for c, r in zip(companies, records)]
        return companies
    return {'company_list': _get_companies()}
