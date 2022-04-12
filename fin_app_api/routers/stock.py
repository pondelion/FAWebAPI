from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import CognitoClaims
from pydantic import BaseModel

# from fin_app_models.dataset import (
#     Stock,
#     StockList,
# )
from fin_app_dataset.services.local_transfered_cache.rs3_to_lrdb.stock import (
    CompanyService,
    StqStockpriceService,
    SectorService,
)

from ..dependencies.auth import get_current_user


class StockpriceParams(BaseModel):
    year: int


router = APIRouter(
    prefix='/stock',
    tags=['stock'],
)

sector_svc = SectorService()
company_svc = CompanyService()
stockprice_svc = StqStockpriceService()


@router.get('/company')
async def get_companies(
    current_user: CognitoClaims = Depends(get_current_user),
):
    companies = [d.__dict__ for d in company_svc.get_all()]
    return {'company_list': companies}


@router.get('/sector')
async def get_sectors(
    current_user: CognitoClaims = Depends(get_current_user),
):
    sectors = [d.__dict__ for d in sector_svc.get_all()]
    return {'sector_list': sectors}


@router.get('/stockprice/{code}')
async def get_stockprice(
    code: int,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    current_user: CognitoClaims = Depends(get_current_user),
):
    if day is not None and month is not None and year is not None:
        df_stockprice = stockprice_svc.get_by_ymd(
            code=code, year=year, month=month, day=day,
        )
    elif month is not None and year is not None:
        df_stockprice = stockprice_svc.get_by_ym(
            code=code, year=year, month=month,
        )
    elif year is not None:
        df_stockprice = stockprice_svc.get_by_y(
            code=code, year=year
        )
    else:
        df_stockprice = stockprice_svc.get_by_code(
            code=code,
        )
    # return {'stockprice': df_stockprice.to_dict(), 'code': code}
    return {
        'stockprice': {col: df_stockprice[col].tolist() for col in df_stockprice.columns},
        'code': code,
    }
