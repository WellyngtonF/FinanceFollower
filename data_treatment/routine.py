import pandas as pd
import numpy as np
import streamlit as st 
import yfinance as yf
from datetime import datetime, timedelta

from data_treatment.yf_func import get_last_price, get_historical_close_price
from dal.rn_rentability import RNRentability
from dal.rn_asset import RNAsset
from dal.rn_category import RNCategory
from dal.rn_sector import RNSector
from dal.rn_operations import RNOperation

rentability = RNRentability()
category = RNCategory()
sector = RNSector()
asset = RNAsset()
operation = RNOperation()

def insert_asset(idasset: int, ticker: str, start_date: str = None, is_usd:bool = False, brl_df: pd.DataFrame = None, end_date: str = None) -> None:
    if start_date == None:
        price = get_last_price(ticker)
        rentability.insert_asset_rentability(idasset, price, datetime.now())
    else:
        data = get_historical_close_price(ticker, start_date, is_usd, brl_df, end_date=end_date)
        if end_date:
            data['Date'] = pd.to_datetime(data['Date'])
            data = data[data['Date'].dt.strftime('%Y-%m-%d') != end_date.strftime('%Y-%m-%d')]
        for _, row in data.iterrows():
            rentability.insert_asset_rentability(idasset, row['Close'], row['Date'])
        
def insert_asset_historical_rentability(initial_date: str = None, end_date: str = None):
    brl_df = get_historical_close_price('BRL=X', operation.get_minimal_operational_date(), end_date=datetime.today().date())
    assets = asset.get_assets_with_date()
    for _, row in assets.iterrows():
        if initial_date <= row['start_date'].date():
            continue
        print(f'Inserindo dado histórico do ativo {row.ticker}')
        start_date = initial_date if initial_date and initial_date > row['start_date'].date() else row['start_date']
        insert_asset(row['idasset'], row['ticker'], start_date, row['is_usd'], brl_df, end_date)

    rentability.insert_parents_historical_rentability(initial_date)

def verify_inserted_rentability() -> None:
    end_date = (datetime.now() - timedelta(1)).date()
    start_date = rentability.get_max_rentability_date()
    diff = end_date - start_date
    days = diff.days
    
    if days > 0:
        initial_date = start_date + timedelta(days)
        insert_asset_historical_rentability(initial_date, end_date=(initial_date + timedelta(1)))