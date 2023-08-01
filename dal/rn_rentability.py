import pandas as pd
import numpy as np
from datetime import datetime

from data_treatment.yf_func import get_array_last_price, get_last_price, get_historical_close_price, get_description_ticker
from dal.rn_base import RNBase
from dal.rn_category import RNCategory
from dal.rn_sector import RNSector
from dal.rn_asset import RNAsset
from dal.rn_capital import RNCapital
from dal.rn_operations import RNOperation
from dal.rn_variables import RNVariable

INSERT_ASSET_RENTABILITY = """
    INSERT INTO asset_rentability (idasset, price, date)
    VALUES (:param1, :param2, :param3)
"""

GET_INITIAL_CATEGORY_DATE = """
    SELECT MIN(date) date
    FROM asset_rentability AR
    INNER JOIN asset A ON A.idasset = AR.idasset
    WHERE A.idcategory = :param1
"""

GET_INITIAL_SECTOR_DATE = """
    SELECT MIN(date) date
    FROM asset_rentability AR
    INNER JOIN asset A ON A.idasset = AR.idasset
    WHERE A.idsector = :param1
"""

GET_MAX_RENTABILITY_DATE = """
    SELECT MAX(date) date
    FROM asset_rentability AR
"""

GET_CATEGORY_RENTABILITY = """
    WITH all_dates AS (
        SELECT DISTINCT date
        FROM asset_rentability
    )

    SELECT a.idcategory, SUM(O.quantity * AR.price) amount, d.date, MAX(C.cash_usd) cash_usd, MAX(C.cash_brl) cash_brl
    FROM asset a
    INNER JOIN category C on C.idcategory = A.idcategory
    CROSS JOIN all_dates AS d
    LEFT JOIN operations o ON a.idasset = o.idasset AND o.direction = 1 AND o.date_operation <= d.date
    INNER JOIN asset_rentability AR ON A.idasset = AR.idasset AND AR.date = d.date
    WHERE A.idcategory = :param1
        AND d.date >= :param2
    GROUP BY a.idcategory, d.date
    ORDER BY d.date;
"""

GET_SECTOR_RENTABILITY = """
    WITH all_dates AS (
        SELECT DISTINCT date
        FROM asset_rentability
    )

    SELECT a.idsector, SUM(O.quantity * AR.price) amount, d.date
    FROM asset a
    CROSS JOIN all_dates AS d
    LEFT JOIN operations o ON a.idasset = o.idasset AND o.direction = 1 AND o.date_operation <= d.date
    INNER JOIN asset_rentability AR ON A.idasset = AR.idasset AND AR.date = d.date
    WHERE A.idsector = :param1
        AND d.date >= :param2
    GROUP BY a.idsector, d.date
    ORDER BY d.date;
"""

GET_WALLET_TOTAL = """
    SELECT date, amount total, idcategory
    FROM category_rentability
"""

GET_ASSET_QUANTITY = """
    SELECT idasset, idcategory, idsector, ticker, description, quantity, average_price, is_usd, (quantity * average_price) invested
    FROM asset
    WHERE quantity > 0
"""

category, sector = [RNCategory(), RNSector()]
asset = RNAsset()
capital = RNCapital()
operation = RNOperation()
variable = RNVariable()

class RNRentability(RNBase):
      
    def insert_asset_rentability(self, idasset, price, date) -> None:
        data = [idasset, price, date]

        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            self.execute_script(INSERT_ASSET_RENTABILITY, data)

        except Exception as e:
            # Handle any errors that occur during the insertion process
            print("Error occurred while inserting rentability:", str(e))

        finally:
            # Close the database connection
            self.close_connection()

    def insert_category_rentability(self, category_id: str, start_date: str) -> None:
        category_rentability = self.select_to_dataframe(GET_CATEGORY_RENTABILITY, [category_id, start_date])

        brl_df = get_historical_close_price('BRL=X', start_date)
        brl_df['Date'] = pd.to_datetime(brl_df['Date'])
        category_rentability['Date'] = pd.to_datetime(category_rentability['date'])
        merged_df = pd.merge(category_rentability, brl_df, how='left', on='Date')
        merged_df['Close'] = merged_df['Close'].fillna(0)
        merged_df['amount'] = merged_df['amount'] + (merged_df['cash_usd'] * merged_df['Close']) + (merged_df['cash_brl'])
        category_rentability = merged_df[['idcategory', 'amount', 'date']]

        self.dataframe_to_db(category_rentability, 'category_rentability')

    def insert_sector_rentability(self, sector_id: str, start_date: str) -> None:
        sector_rentability = self.select_to_dataframe(GET_SECTOR_RENTABILITY, [sector_id, start_date])
        self.dataframe_to_db(sector_rentability, 'sector_rentability')

    def insert_parents_historical_rentability(self, initial_date: str = None) -> None:
        try:
            self.create_connection()

            categorys_df = category.get_categorys()

            for category_id in categorys_df['id']:
                start_date = initial_date if initial_date else self.select_to_dataframe(GET_INITIAL_CATEGORY_DATE, category_id)['date'][0]
                if start_date != None:
                    self.insert_category_rentability(category_id, start_date)

            sector_df = sector.get_sectors()

            for sector_id in sector_df['id']:
                start_date = initial_date if initial_date else self.select_to_dataframe(GET_INITIAL_SECTOR_DATE, sector_id)['date'][0]

                if start_date != None:
                    self.insert_sector_rentability(sector_id, start_date)

        except Exception as e:
            print("Error occurred while inserting rentability:", str(e))
        finally:
            self.close_connection()

    def get_wallet_total(self, category_id:str = None) -> pd.DataFrame:
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_WALLET_TOTAL)

            if category_id:
                df = df[df['idcategory'] == category_id]

            df = df.groupby('date')['total'].sum().reset_index()
            df['date'] = pd.to_datetime(df['date'])
            df['date'] = df['date'].dt.tz_localize('America/Sao_Paulo')
        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while selecting total of wallet:", str(e))

        finally:
            self.close_connection()

        return df
    
    def get_percentile_wallet(self, category_id: str = None):
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_ASSET_QUANTITY)

            if category_id:
                df = df[df['idcategory'] == category_id]

            df['price'] = get_array_last_price(np.array(df['ticker']))

            df['usdbrl'] = get_last_price('BRL=X')

            df['amount'] = df['quantity'] * df['price']
            
            df['amount'] = df.apply(lambda row: row['amount'] * row['usdbrl'] if row['is_usd'] == 1 else row['amount'], axis=1)

            return df

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while calculating the percentile for each asset in wallet:", str(e))

        finally:
            self.close_connection()

        return df
    
    def get_category_percentile(self, assets: pd.DataFrame) -> pd.DataFrame:
        try:
            assets = self.get_percentile_wallet()
            self.create_connection()

            category_df = category.get_categorys()

            assets = assets.groupby('idcategory')['amount'].sum().reset_index()

            category_df = pd.merge(category_df, assets, left_on='id', right_on='idcategory', how='inner')

            category_df['usdbrl'] = get_last_price('BRL=X')

            category_df['amount'] = category_df['amount'] + category_df['Caixa R$'] + (category_df['Caixa $'] * category_df['usdbrl'])

        except Exception as e:
            category_df = pd.DataFrame([])
            print("Error occurred while calculating the percentile for each category in wallet:", str(e))

        finally:
            self.close_connection()

        return category_df
    
    def get_sector_percentile(self, assets: pd.DataFrame, category_id: str) -> pd.DataFrame:
        try:
            assets = self.get_percentile_wallet()
            self.create_connection()

            sector_df = sector.get_sector_by_idcategory(category_id)
            
            assets = assets.fillna(value={'idsector': 0})
            if category_id:
                assets = assets[assets['idcategory'] == category_id]

            assets = assets.groupby('idsector')['amount'].sum().reset_index()

            sector_df = pd.merge(assets, sector_df, left_on='idsector', right_on='idsector', how='left')

            sector_df = sector_df.fillna(value={'description': 'Nenhum'})

        except Exception as e:
            sector_df = pd.DataFrame([])
            print("Error occurred while calculating the percentile for each sector in wallet:", str(e))

        finally:
            self.close_connection()

        return sector_df
    
    def get_rentability(self, id_category: str = None) -> pd.DataFrame:
        try:
            df_wallet_total = self.get_wallet_total(id_category)
            df_capital = capital.get_capital_injection(id_category)
            df_capital['date'] = pd.to_datetime(df_capital['date'])
            df_capital['date'] = df_capital['date'].dt.tz_localize('America/Sao_Paulo')
            
            df = pd.merge(df_wallet_total, df_capital.groupby('date')['amount'].sum().cumsum().reset_index(),
                     on='date', how='left')
            
            df['date'] = pd.to_datetime(df['date'])
            
            df['amount'] = df['amount'].fillna(0)

            df['amount'] = df['amount'].cummax()

            df['Carteira'] = (df['total'] / df['amount'] - 1) 

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while calculating the wallet rentability:", str(e))

        finally:
            self.close_connection()

        return df
    
    def get_benchmark_rentability(self, benchmark: str) :
        try:
            start_date = operation.get_minimal_operational_date()
            df = get_historical_close_price(benchmark,start_date.date())
            bench_name = get_description_ticker(benchmark)
            # Calculate the daily rentability
            df['rentability'] = df['Close'].pct_change() * 100
            df['Date'] = pd.to_datetime(df['Date'])
            df['Date'] = df['Date'].dt.tz_localize('America/Sao_Paulo')
            df = df.sort_values('Date')

            # Calculate the cumulative rentability
            df[bench_name] = (1 + df['rentability'] / 100).cumprod() - 1
            df[bench_name] = df[bench_name].fillna(0)

            df = df.drop(['rentability'], axis=1)

        except Exception as e:
            df = pd.DataFrame([])
            print(f"Error occurred while calculating {benchmark} rentability:", str(e))

        return df, bench_name
    
    def get_month_rentability(self) -> pd.DataFrame:
        try:
            daily_rentability = self.get_rentability().sort_values('date')
            daily_rentability['date'] = pd.to_datetime(daily_rentability['date'])
            daily_rentability = daily_rentability.rename(columns={'total': 'actual value', 'amount': 'value invested'})

            df = daily_rentability.groupby(pd.Grouper(key='date', freq='M')).apply(
                lambda x: (x.iloc[-1]['actual value'] / (
                    daily_rentability.loc[daily_rentability['date'] < x.iloc[0]['date'], 'actual value'].iloc[-1] + x['value invested'].diff().sum()
                )) - 1
                if x.index[0] != daily_rentability.index[0]
                else (x.iloc[-1]['actual value'] / x.iloc[-1]['value invested']) - 1
            )

            df = df.reset_index().rename(columns={'date': 'month', 0: 'rentability'})

            df['month'] = df['month'].apply(lambda x: x.strftime('%b'))

            months = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M').strftime('%b')

            all_months_df = pd.DataFrame({'month': months})

            df = all_months_df.merge(df, on='month', how='left')

            df['rentability'] = df['rentability'].fillna(0)

            df = df.sort_index()
        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while calculating the month rentability:", str(e))

        return df
    
    def get_cash(self) -> float:
        try:
            df = category.get_categorys()
            df['usdbrl'] = get_last_price('BRL=X')

            cash = df['Caixa R$'].sum() + (df['Caixa $'] * df['usdbrl']).sum()

        except Exception as e:
            cash = 0
            print("Error occurred while calculating the cash data:", str(e))

        return cash

    def get_general_waterfall_data(self) -> pd.DataFrame:
        try:
            df = self.get_percentile_wallet()

            invested = capital.get_capital_injection()['amount'].sum()

            df['usdbrl'] = float(variable.get_variable('usd_dca'))

            df['invested'] = df.apply(lambda row: row['invested'] * row['usdbrl'] if row['is_usd'] == 1 else row['invested'], axis=1)
            df['PnL'] = df['amount'] - df['invested']

            df['wf_data'] = ((invested + df['PnL']) / invested) - 1

            df = df[['description', 'wf_data']]
        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while calculating the waterfall data:", str(e))

        return df
    
    def get_categorys_rentability(self, assets: pd.DataFrame) -> pd.DataFrame:
        try:    
            grouped_df = assets.groupby('idcategory').agg({'invested': 'sum', 'amount': 'sum', 'is_usd': 'max'})
            category_df = category.get_categorys()

            df = pd.merge(category_df, grouped_df, left_on='id', right_on='idcategory', how='inner').sort_values('amount', ascending=False)

            df['usdbrl'] = get_last_price('BRL=X')

            df['amount'] = df['amount'] + df['Caixa R$'] + (df['Caixa $'] * df['usdbrl'])
            df['usd_dca'] = float(variable.get_variable('usd_dca'))
            df['invested_usd'] = df.apply(lambda row: row['invested'] if row['is_usd'] == 1 else 0, axis= 1)
            df['invested'] = df.apply(lambda row: row['invested'] * row['usd_dca'] if row['is_usd'] == 1 else row['invested'], axis=1)
            df['invested'] = df['invested'] + df['Caixa R$'] + (df['Caixa $'] * df['usd_dca'])
            df['rentability'] = ((df['amount'] / df['invested']) - 1) * 100

            df = df.rename(columns={'invested': 'Investido (R$)', 'invested_usd': 'Investido ($)', 'amount': 'Atual (R$)', 'rentability': 'Rentabilidade'})

            df = df[['Categoria', 'Investido ($)', 'Investido (R$)', 'Atual (R$)', 'Rentabilidade']]

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occured while calculating the category rentability table:", str(e))

        return df
    
    def get_assets_rentability(self, asset: pd.DataFrame) -> pd.DataFrame:
        try:    
            df = asset.copy().sort_values('amount', ascending=False)
            df['usdbrl'] = get_last_price('BRL=X')

            df['usd_dca'] = float(variable.get_variable('usd_dca'))
            df['invested_usd'] = df.apply(lambda row: row['invested'] if row['is_usd'] == 1 else 0, axis= 1)
            df['invested'] = df.apply(lambda row: row['invested'] * row['usd_dca'] if row['is_usd'] == 1 else row['invested'], axis=1)
            df['rentability'] = ((df['amount'] / df['invested']) - 1) * 100

            df = df.rename(columns={
                'description': 'Ativo', 'invested': 'Investido (R$)', 'invested_usd': 'Investido ($)', 
                'amount': 'Atual (R$)', 'rentability': 'Rentabilidade'})

            if df['is_usd'].max() == 1:
                df = df.rename(columns={'average_price': 'Preço médio ($)', 'price': 'Preço Atual ($)'})
                df = df[['Ativo', 'Preço médio ($)', 'Preço Atual ($)', 'Investido ($)', 'Investido (R$)', 'Atual (R$)', 'Rentabilidade']]
            else:
                df = df.rename(columns={'average_price': 'Preço médio (R$)', 'price': 'Preço Atual (R$)'})
                df = df[['Ativo', 'Preço médio (R$)', 'Preço Atual (R$)', 'Investido (R$)', 'Atual (R$)', 'Rentabilidade']]

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occured while calculating the category rentability table:", str(e))

        return df
    
    def get_max_rentability_date(self) -> None:
        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            df = self.select_to_dataframe(GET_MAX_RENTABILITY_DATE)

            date = df['date'][0]

        except Exception as e:
            date = None
            print("Error occurred while getting max rentability date:", str(e))

        finally:
            # Close the database connection
            self.close_connection()
        
        return date