from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import CognitoClaims

from fin_app_dataset.services.local_transfered_cache.rs3_to_lrdb.stock import (
    StqStockpriceService,
)

from ..dependencies.auth import get_current_user
from ..utils.time_record import time_record


router = APIRouter(
    prefix='/stockprice',
    tags=['Storckprice API'],
)

stockprice_svc = StqStockpriceService()


@router.get('/{code}')
async def get_stockprice(
    code: int,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    current_user: CognitoClaims = Depends(get_current_user),
):
    @time_record
    def _get_stockprice():
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
        return df_stockprice
    df_stockprice = _get_stockprice()
    # return {'stockprice': df_stockprice.to_dict(), 'code': code}
    RETURN_COLS = ['date', 'open', 'high', 'low', 'close', 'volume']
    return {
        'stockprice': {col: df_stockprice[col].tolist() for col in RETURN_COLS},
        'code': code,
    }
