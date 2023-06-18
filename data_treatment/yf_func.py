import pandas as pd
import numpy as np
from datetime import timedelta, datetime, date
import logging
import yfinance as yf

logging.getLogger('yfinance').setLevel(logging.CRITICAL)
        
def get_previous_trading_data(ticker: yf.Ticker, date) -> pd.DataFrame:
    end_date = date + timedelta(1)
    try:
        data = ticker.history(start=date, end=end_date)
    except IndexError as e:
        data = pd.DataFrame([])

    if data.empty:
        date = date - timedelta(days=1)
        data = get_previous_trading_data(ticker, date)
    return data

def get_last_price(symbol: str):
    ticker = yf.Ticker(symbol)
    last_price = ticker.info['currentPrice'] if 'currentPrice' in ticker.info else ticker.fast_info['lastPrice']
    return last_price

def get_array_last_price(ticker_arr: np.array) -> np.array:
    data = []
    for ticker in ticker_arr:
        price = get_last_price(ticker)
        data.append(price)

    return data

def get_historical_close_price(symbol: str, start_date: str, is_usd: bool = False, brl_df: pd.DataFrame = None, end_date: str = None):
    end_date = end_date if end_date else (datetime.today() - timedelta(days=1)).date()
    # start_date = datetime.strptime('2023-03-01', '%Y-%m-%d')
    # end_date = datetime.strptime('2023-03-05', '%Y-%m-%d')
    ticker = yf.Ticker(symbol)
    try:
        hist = ticker.history(start=start_date, end=end_date)
    except IndexError as e:
        print("Não foram encontrado dados para a data atual, recuperando fechamento do dia anterior")
        hist = get_previous_trading_data(ticker, start_date - timedelta(1))

    if hist.empty and (end_date - start_date).days <= 1:
        hist = get_previous_trading_data(ticker, start_date - timedelta(1))
        hist['Date'] = start_date
    else:
        hist['Date'] = hist.index
        hist['Date'] = hist['Date'].dt.date

    # Check for missing data and fill with previous trading day's data
    current_date = start_date if type(start_date) == date else start_date.date()
    while current_date <= end_date:
        if current_date not in np.array(hist['Date']):
            previous_trading_day = current_date - timedelta(days=1)
            previous_data = get_previous_trading_data(ticker, previous_trading_day)
            previous_data['Date'] = current_date.strftime('%Y-%m-%d')
            hist = pd.concat([hist, previous_data])
        current_date += timedelta(days=1)

    hist.index.name = 'index'

    if is_usd: 
        brl_df['Date'] = pd.to_datetime(brl_df['Date']).dt.date
        hist = pd.merge(hist, brl_df, how='left', on='Date')
        hist['Close'] = hist['Close_x'] * hist['Close_y']

    hist = hist.reset_index().drop_duplicates()

    return hist[['Date', 'Close']]

def get_description_ticker(symbol: str) -> str:
    ticker = yf.Ticker(symbol)
    return ticker.info['longName']