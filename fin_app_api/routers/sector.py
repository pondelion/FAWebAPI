from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import CognitoClaims

from fin_app_dataset.services.local_transfered_cache.rs3_to_lrdb.stock import (
    SectorService,
)

from ..dependencies.auth import get_current_user
from ..utils.time_record import time_record


router = APIRouter(
    prefix='/sector',
    tags=['Sector API'],
)

sector_svc = SectorService()


@router.get('/')
async def get_sectors(
    current_user: CognitoClaims = Depends(get_current_user),
):
    sectors = [d.__dict__ for d in sector_svc.get_all()]
    return {'sector_list': sectors}
