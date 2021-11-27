from fastapi import APIRouter, Depends
from fastapi_cloudauth.cognito import CognitoClaims
from fin_app_models.dataset import (
    Stock,
    StockList,
)

from ..dependencies.auth import get_current_user


router = APIRouter(
    prefix='/stock',
    tags=['stock'],
)
df_stocklist = StockList().data
stocklist = df_stocklist.apply(lambda x: {
    'company_name': x['銘柄名'].replace('(株)', ''),
    'ticker': x['銘柄コード'],
    'sector': x['業種分類']
}, axis=1).to_list()


@router.get('/')
async def get_stocks(
    current_user: CognitoClaims = Depends(get_current_user),
):
    return {'stocklist': stocklist}
