import pandas as pd
from datetime import datetime

from dal.rn_base import RNBase

GET_ALL_CATEGORYS = """
    SELECT idcategory, description, cash_brl, cash_usd, benchmark
    FROM category
"""

GET_CATEGORY_FROM_ID = """
    SELECT idcategory, description, cash_brl, cash_usd, benchmark
    FROM category
    WHERE idcategory = :param1
"""

INSERT_CATEGORY = """
    INSERT INTO category (description, cash_brl, cash_usd, benchmark, insert_date, update_date)
    VALUES (:param1, :param2, :param3, :param4, :param5, :param6)
"""

UPDATE_CATEGORY = """
    UPDATE category
    SET description = :param1,
        cash_brl = :param2,
        cash_usd = :param3,
        benchmark = :param4,
        update_date = :param5
    WHERE idcategory = :param6
"""

DELETE_CATEGORY = """
    DELETE FROM category
    WHERE idcategory = :param1
"""

column_mapping = {
    'idcategory': 'id',
    'description': 'Categoria',
    'cash_brl': 'Caixa R$',
    'cash_usd': 'Caixa $',
    'benchmark': 'Benchmark'
}

class RNCategory(RNBase):
    def modeling_column(self, df: pd.DataFrame) -> pd.DataFrame:
        renamed_df = df.rename(columns=column_mapping)

        return renamed_df
    
    def get_categorys(self) -> pd.DataFrame:
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_ALL_CATEGORYS)

            df = self.modeling_column(df)

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while selecting category:", str(e))

        finally:
            self.close_connection()

        return df

    def insert_category(self, description, cash_brl, cash_usd, benchmark) -> None:
        # Get the current datetime
        current_datetime = datetime.now()

        data = [description, cash_brl, cash_usd, benchmark, current_datetime, current_datetime]

        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            self.execute_script(INSERT_CATEGORY, data)

        except Exception as e:
            # Handle any errors that occur during the insertion process
            print("Error occurred while inserting category:", str(e))

        finally:
            # Close the database connection
            self.close_connection()

    def get_category_by_id(self, category_id) -> pd.DataFrame:
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_CATEGORY_FROM_ID, category_id)

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while updating category:", str(e))

        finally:
            self.close_connection()

        return df
    
    def edit_category(self, description, cash_brl, cash_usd, benchmark, category_id) -> pd.DataFrame:

        current_datetime = datetime.now()

        data = [description, cash_brl, cash_usd, benchmark, current_datetime, category_id]
        print(data)

        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            self.execute_script(UPDATE_CATEGORY, data)

        except Exception as e:
            # Handle any errors that occur during the insertion process
            print("Error occurred while editing category:", str(e))

        finally:
            # Close the database connection
            self.close_connection()

    def delete_category(self, category_id) -> None:
        try:
            self.create_connection()
            self.execute_script(DELETE_CATEGORY, category_id)

        except Exception as e:
            print("Error occurred while deleting category:", str(e))

        finally:
            self.close_connection()