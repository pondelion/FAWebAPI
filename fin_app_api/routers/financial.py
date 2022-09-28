from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import CognitoClaims

from fin_app_dataset.services.local_transfered_cache.rs3_to_lrdb.financial import (
    YFFinancialService,
)

from ..dependencies.auth import get_current_user
from ..utils.time_record import time_record


router = APIRouter(
    prefix='/financial',
    tags=['Company Financial API'],
)

financial_svc = YFFinancialService()


@router.get('/{code}')
async def get_financial(
    code: int,
    year: Optional[int] = None,
    month: Optional[int] = None,
    day: Optional[int] = None,
    current_user: CognitoClaims = Depends(get_current_user),
):
    @time_record
    def _get_financial():
        if day is not None and month is not None and year is not None:
            df_financial = financial_svc.get_by_ymd(
                code=code, year=year, month=month, day=day,
            )
        elif month is not None and year is not None:
            df_financial = financial_svc.get_by_ym(
                code=code, year=year, month=month,
            )
        elif year is not None:
            df_financial = financial_svc.get_by_y(
                code=code, year=year
            )
        else:
            df_financial = financial_svc.get_by_code(
                code=code,
            )
        return df_financial
    df_financial = _get_financial()
    # return {'stockprice': df_financial.to_dict(), 'code': code}
    RETURN_COLS = df_financial.columns.tolist()
    return {
        'financial': {col: df_financial[col].tolist() for col in RETURN_COLS},
        'code': code,
    }
