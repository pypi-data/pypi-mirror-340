# todo 1. 对于查询的持仓，空的也要推送空的，否则orderplit无法回调.  这对于http请求很容易实现，但是如果是websocket回调，也许空的不会回调？例如ibk

import pandas as pd
from pandas import DataFrame
from datetime import datetime, timedelta
from ks_trade_api.base_fundamental_api import BaseFundamentalApi
from ks_trade_api.utility import extract_vt_symbol, generate_vt_symbol
from ks_trade_api.constant import Exchange, SubExchange, RET_OK, RET_ERROR, Product
from ks_utility.datetimes import get_date_str
from ks_utility import datetimes
import sys
from decimal import Decimal
import uuid
from logging import DEBUG, WARNING, ERROR
from ks_utility.numbers import to_decimal
from enum import Enum

from .EmQuantAPI import c

class MyCurrency(Enum):
    CNY = 2
    USD = 3
    HKD = 4

class MyExchange(Enum):
    SH = 'SH'
    SZ = 'SZ'
    HK = 'HK'
    BJ = 'BJ'

    N = 'N'
    O = 'O'
    A = 'A'
    F = 'F'

EXCHANGE2MY_CURRENCY = {
    Exchange.SSE: MyCurrency.CNY,
    Exchange.SZSE: MyCurrency.CNY,
    Exchange.BSE: MyCurrency.CNY,
    Exchange.SEHK: MyCurrency.HKD,
    Exchange.SMART: MyCurrency.USD
}

EXCHANGE_KS2MY = {
    Exchange.SSE: MyExchange.SH,
    Exchange.SZSE: MyExchange.SZ,
    Exchange.SEHK: MyExchange.HK,
    Exchange.BSE: MyExchange.BJ
}
EXCHANGE_MY2KS = {v:k for k,v in EXCHANGE_KS2MY.items()}
EXCHANGE_MY2KS[MyExchange.A] = Exchange.SMART
EXCHANGE_MY2KS[MyExchange.O] = Exchange.SMART
EXCHANGE_MY2KS[MyExchange.N] = Exchange.SMART
EXCHANGE_MY2KS[MyExchange.F] = Exchange.SMART

EXCHANGE_MY2KS_SUB = {
    MyExchange.A: SubExchange.US_AMEX,
    MyExchange.O: SubExchange.US_NASDAQ,
    MyExchange.N: SubExchange.US_NYSE,
    MyExchange.F: SubExchange.US_PINK,

    MyExchange.SH: SubExchange.CN_SH,
    MyExchange.SZ: SubExchange.CN_SZ,
    MyExchange.BJ: SubExchange.CN_BJ,

    MyExchange.HK: SubExchange.HK_MAINBOARD
}

EXCHANGE_KS2MY_SUB = {v:k for k,v in EXCHANGE_MY2KS_SUB.items()}
EXCHANGE_KS2MY_SUB[SubExchange.CN_STIB] = MyExchange.SH
EXCHANGE_KS2MY_SUB[SubExchange.HK_GEMBOARD] = MyExchange.HK
EXCHANGE_KS2MY_SUB[SubExchange.HK_HKEX] = MyExchange.HK
EXCHANGE_KS2MY_SUB[SubExchange.HK_MAINBOARD] = MyExchange.HK

PERCENT_COLUMNS = ['ROE', 'ROETTM', 'DIVIDENDTTM', 'DIVIDENDYIELDY', 'PE', 'PB']

# 标准字段映射
INDICATORS_KS2MY = {
    # ROE (chice面板上，沪深股票是ROEWA；港股是ROEAVG)
    'ROE.SSE': 'ROEAVG',
    'ROE.SZSE': 'ROEAVG',
    'ROE.BSE': 'ROEAVG',
    'ROE.SEHK': 'ROEAVG',
    'ROE.SMART': 'ROEAVG',
    
    # 资产负债率 
    'LIBILITYTOASSET.SSE': 'LIBILITYTOASSETRPT',
    'LIBILITYTOASSET.SZSE': 'LIBILITYTOASSETRPT',
    'LIBILITYTOASSET.BSE': 'LIBILITYTOASSETRPT',
    'LIBILITYTOASSET.SEHK': 'LIBILITYTOASSET',
    'LIBILITYTOASSET.SMART': 'LIBILITYTOASSET',

    # 股利支付率
    'DIVANNUPAYRATE.SSE': 'DIVANNUPAYRATE',
    'DIVANNUPAYRATE.SZSE': 'DIVANNUPAYRATE',
    'DIVANNUPAYRATE.BSE': 'DIVANNUPAYRATE',
    'DIVANNUPAYRATE.SEHK': 'DIVANNUACCUMRATIO',
    'DIVANNUPAYRATE.SMART': 'DIVANNUACCUMRATIO',

    # 市值，流通市值
    'MV.SSE': 'MV',
    'MV.SZSE': 'MV',
    'MV.BSE': 'MV',
    'MV.SEHK': 'MV',
    'MV.SMART': 'MV',
    
    'CIRCULATEMV.SSE': 'CIRCULATEMV',
    'CIRCULATEMV.SZSE': 'CIRCULATEMV',
    'CIRCULATEMV.BSE': 'CIRCULATEMV',
    'CIRCULATEMV.SEHK': 'LIQMV',
    'CIRCULATEMV.SMART': 'LIQMV',

    # PE, PB
    'PE.SSE': 'PELYR',
    'PE.SZSE': 'PELYR',
    'PE.BSE': 'PELYR',
    'PE.SEHK': 'PELYR',
    'PE.SMART': 'PELYR',

    'PB.SSE': 'PBMRQ',
    'PB.SZSE': 'PBMRQ',
    'PB.BSE': 'PBMRQ',
    'PB.SEHK': 'PBMRQ',
    'PB.SMART': 'PBMRQ',
    
    # Year-over-Year Operating Revenue (营业收入同比增长)
    'YOYOR.SSE': 'YOYOR',
    'YOYOR.SZSE': 'YOYOR',
    'YOYOR.BSE': 'YOYOR',
    'YOYOR.SEHK': 'GR1YGROWTHRATE',
    'YOYOR.SMART': 'GR1YGROWTHRATE',
    
    # Year-over-Year Net Income (净利润同比增长)
    'YOYNI.SSE': 'YOYNI',
    'YOYNI.SZSE': 'YOYNI',
    'YOYNI.BSE': 'YOYNI',
    'YOYNI.SEHK': 'YOYNI',
    'YOYNI.SMART': 'YOYNI',
    
    # Compound Annual Growth Rate Total Operating revenue (总营业收入复合增长率)
    'CAGRTOR.SSE': 'CAGRGR',
    'CAGRTOR.SZSE': 'CAGRGR',
    'CAGRTOR.BSE': 'CAGRGR',
    'CAGRTOR.SEHK': 'CAGRGR',
    'CAGRTOR.SMART': 'CAGRGR',
}

INDICATORS_MY2KS = {v:'.'.join(k.split('.')[:-1]) for k,v in INDICATORS_KS2MY.items()}

EXCHANGE_PRODUCT2PUKEYCODE = {
    'CNSE.EQUITY': '001071',
    'SEHK.EQUITY': '401001',
    'SMART.EQUITY': '202001004',

    'CNSE.ETF': '507001',
    'SEHK.ETF': '404004',
    'SMART.ETF': '202003009'
}

def extract_my_symbol(my_symbol):
    items = my_symbol.split(".")
    return '.'.join(items[:-1]), MyExchange(items[-1])

def symbol_ks2my(vt_symbol: str, sub_exchange: SubExchange = None):
    if not vt_symbol:
        return ''
    symbol, ks_exchange = extract_vt_symbol(vt_symbol)
    symbol = symbol.replace('.', '_')
    if not sub_exchange:
        my_symbol = generate_vt_symbol(symbol, EXCHANGE_KS2MY.get(ks_exchange))
    else:
        my_symbol = generate_vt_symbol(symbol, EXCHANGE_KS2MY_SUB.get(sub_exchange))
    return my_symbol

def symbol_my2ks(my_symbol: str):
    if not my_symbol:
        return ''
    symbol, my_exchange = extract_my_symbol(my_symbol)
    symbol = symbol.replace('_', '.') # 东财使用下划线，而我们根据futu的用了.
    return generate_vt_symbol(symbol, EXCHANGE_MY2KS.get(my_exchange))

def symbol_my2sub_exchange(my_symbol: str):
    if not my_symbol:
        return ''
    symbol, my_exchange = extract_my_symbol(my_symbol)
    try:
        EXCHANGE_MY2KS_SUB.get(my_exchange).value
    except:
        breakpoint()
    return EXCHANGE_MY2KS_SUB.get(my_exchange).value

class KsEastmoneyFundamentalApi(BaseFundamentalApi):
    gateway_name: str = "KS_EASTMONEY_FUNDAMENTAL"

    def __init__(self, setting: dict):
        dd_secret = setting.get('dd_secret')
        dd_token = setting.get('dd_token')
        gateway_name = setting.get('gateway_name', self.gateway_name)
        super().__init__(gateway_name=gateway_name, dd_secret=dd_secret, dd_token=dd_token)

        self.setting = setting
        self.login()

    def login(self):
        username = self.setting.get('username')
        password = self.setting.get('password')
        startoptions = "ForceLogin=1" + ",UserName=" + username + ",Password=" + password;
        loginResult = c.start(startoptions, '')
        self.log(loginResult, '登录结果')

    def _normalization_indicators_input(self, indicators: str, exchange: Exchange):
        indicators_list = indicators.split(',')
        indicators_new = [INDICATORS_KS2MY.get(f'{x}.{exchange.value}', x) for x in indicators_list]
        return ','.join(indicators_new)
    
    def _normalization_indicators_output(self, df: DataFrame):
        rename_columns = {x:INDICATORS_MY2KS[x] for x in df.columns if x in INDICATORS_MY2KS}
        return df.rename(columns=rename_columns)

    # 暂时不支持跨市场多标的，使用第一个表的市场来决定所有标的的市场
    # sub_exchange是用来做美股区分，东财
    def css(self, vt_symbols: list[str], indicators: str = '', options: str = '', sub_exchanges: list[str] = []) -> pd.DataFrame:
        if not vt_symbols:
            return None
        
        symbol, exchange = extract_vt_symbol(vt_symbols[0])
        
        indicators = self._normalization_indicators_input(indicators, exchange)

        # 默认pandas返回
        if not 'IsPandas' in options:
            options += ',IsPandas=1'

        if not 'TradeDate' in options:
            options += f',TradeDate={get_date_str()}'

        year = datetimes.now().year
        if not 'Year' in options:      
            options += f',Year={year}'

        if not 'PayYear' in options:
            options += f',PayYear={year}'

        if not 'ReportDate' in options:
            options += ',ReportDate=MRQ'

        if not 'CurType' in options:
            options += f',CurType={EXCHANGE2MY_CURRENCY.get(exchange).value}'

        if 'ROETTM' in indicators:
            options += ',TtmType=1'

        if 'LIBILITYTOASSETRPT' in indicators:
            options += ',Type=3' # 合并报表（调整后）

        # if 'BPS' in indicators:
        #     options += f',CurType={EXCHANGE2MY_CURRENCY.get(exchange).value}'

        my_symbols = [symbol_ks2my(x, SubExchange(sub_exchanges[i]) if len(sub_exchanges) and sub_exchanges[i] else None) for i,x in enumerate(vt_symbols)]
        df = c.css(my_symbols, indicators=indicators, options=options)
        if isinstance(df, c.EmQuantData):
            return RET_ERROR, str(df)
        
        df.reset_index(drop=False, inplace=True)

        # 转换symbol
        df['CODES'] = df['CODES'].transform(symbol_my2ks)
        df.rename(columns={'CODES': 'vt_symbol'}, inplace=True)

        # LIBILITYTOASSET: 港美的是百分号，A股是小数
        if 'LIBILITYTOASSET' in df.columns:
            is_cn = df.vt_symbol.str.endswith('.SSE') | df.vt_symbol.str.endswith('.SZSE') | df.vt_symbol.str.endswith('.BSE')
            df.loc[is_cn, 'LIBILITYTOASSET'] = df[is_cn]['LIBILITYTOASSET'] * 100

        df = self._normalization_indicators_output(df)

        # 转换百分比 # 20241223不再转换百分比，因为约定俗称就是用百分比
        # for column in PERCENT_COLUMNS:
        #     if column in df.columns:
        #         df[column] = df[column] / 100

        return RET_OK, df
    
    def sector(self, exchange: Exchange, products: list[Product], tradedate: str = None):
        if not tradedate:
            tradedate = get_date_str()
        # 默认pandas返回
        options = 'IsPandas=1'

        all_df = pd.DataFrame()
        for product in products:
            pukeycode = EXCHANGE_PRODUCT2PUKEYCODE.get(f'{exchange.name}.{product.name}')
            df = c.sector(pukeycode, tradedate, options)
            df['vt_symbol'] = df['SECUCODE'].transform(symbol_my2ks)
            df['sub_exchange'] = df['SECUCODE'].transform(symbol_my2sub_exchange)
            df['name'] = df['SECURITYSHORTNAME']
            df['product'] = product.name

            all_df = pd.concat([all_df, df[['vt_symbol', 'name', 'sub_exchange', 'product']]], ignore_index=True)
        return RET_OK, all_df

    # 关闭上下文连接
    def close(self):
        pass
        # self.quote_ctx.close()
        # self.trd_ctx.close()


        