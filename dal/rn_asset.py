import pandas as pd
from datetime import datetime

from dal.rn_base import RNBase

GET_ALL_ASSETS = """
    SELECT A.idasset, C.description category_description, IFNULL(S.description, 'Nenhum') sector_description,
        A.ticker, A.description
    FROM asset A
    INNER JOIN category C ON C.idcategory = A.idcategory
    LEFT JOIN sector S ON S.idsector = A.idsector
"""

INSERT_ASSET = """
    INSERT INTO asset (idcategory, idsector, description, ticker, is_usd, insert_date, update_date)
    VALUES (:param1, :param2, :param3, :param4, :param5, :param6, :param7)
"""

GET_ASSET_FROM_ID = """
    SELECT idasset, idsector, idcategory, ticker, description, is_usd
    FROM asset
    WHERE idasset = :param1
"""

UPDATE_ASSET = """
    UPDATE asset
    SET idcategory = :param1,
        idsector = :param2,
        description = :param3,
        ticker = :param4,
        is_usd = :param5,
        update_date = :param6
    WHERE idasset = :param7
"""

DELETE_ASSET = """
    DELETE FROM asset
    WHERE idasset = :param1
"""

GET_ALL_ASSETS_R = """
    SELECT A.idasset, A.ticker, A.description, A.is_usd, MIN(O.date_operation) start_date
    FROM asset A
    INNER JOIN operations O ON O.idasset = A.idasset
    GROUP BY A.idasset, A.ticker, A.description, A.is_usd
"""

column_mapping = {
    'idasset': 'id',
    'category_description': 'Categoria',
    'sector_description': 'Setor',
    'ticker': 'Simbolo',
    'description': 'Ativo',
}

class RNAsset(RNBase):
    def modeling_column(self, df: pd.DataFrame) -> pd.DataFrame:
        renamed_df = df.rename(columns=column_mapping)

        return renamed_df
    
    def get_assets(self) -> pd.DataFrame:
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_ALL_ASSETS)

            df = self.modeling_column(df)

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while selecting asset:", str(e))

        finally:
            self.close_connection()

        return df
    
    def insert_asset(self, idcategory, idsector, description, ticker, is_usd) -> None:
        # Get the current datetime
        current_datetime = datetime.now()

        data = [idcategory, idsector, description, ticker, is_usd, current_datetime, current_datetime]

        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            self.execute_script(INSERT_ASSET, data)

        except Exception as e:
            # Handle any errors that occur during the insertion process
            print("Error occurred while inserting asset:", str(e))

        finally:
            # Close the database connection
            self.close_connection()

    def get_asset_by_id(self, asset_id) -> pd.DataFrame:
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_ASSET_FROM_ID, asset_id)

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while updating asset:", str(e))

        finally:
            self.close_connection()

        return df
    
    def edit_asset(self, category_id, sector_id, description, ticker, is_usd, asset_id) -> pd.DataFrame:

        current_datetime = datetime.now()

        data = [category_id, sector_id, description, ticker, is_usd, current_datetime, asset_id]

        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            self.execute_script(UPDATE_ASSET, data)

        except Exception as e:
            # Handle any errors that occur during the insertion process
            print("Error occurred while inserting asset:", str(e))

        finally:
            # Close the database connection
            self.close_connection()

    def delete_asset(self, asset_id) -> None:
        try:
            self.create_connection()
            self.execute_script(DELETE_ASSET, asset_id)

        except Exception as e:
            print("Error occurred while deleting asset:", str(e))

        finally:
            self.close_connection()

    def get_assets_with_date(self) -> pd.DataFrame:
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_ALL_ASSETS_R)

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while selecting asset:", str(e))

        finally:
            self.close_connection()

        return df