import pandas as pd
from datetime import datetime

from dal.rn_base import RNBase
from dal.rn_variables import RNVariable

INSERT_CAPITAL = """
    INSERT INTO capital_injection (amount, injection_date, insert_date, update_date)
    VALUES (:param1, :param2, :param3, :param4)
"""

GET_ALL_CAPITAL_INJ = """
    SELECT CAST(injection_date AS DATE) date, amount
    FROM capital_injection
"""

GET_INVESTED_CATEGORY = """
    SELECT CAST(O.date_operation AS DATE) date, SUM(O.quantity * O.price) amount, A.is_usd
    FROM operations O
    INNER JOIN asset A on A.idasset = O.idasset
    WHERE A.idcategory = :param1
    GROUP BY O.date_operation,
        A.is_usd
"""

class RNCapital(RNBase):    
    def insert_capital(self, amount, injection_date) -> None:
        # Get the current datetime
        current_datetime = datetime.now()

        data = [amount, injection_date, current_datetime, current_datetime]

        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            self.execute_script(INSERT_CAPITAL, data)

        except Exception as e:
            # Handle any errors that occur during the insertion process
            print("Error occurred while inserting asset:", str(e))

        finally:
            # Close the database connection
            self.close_connection()

    def get_capital_injection(self, category_id:str = None) -> pd.DataFrame:
        try:
            self.create_connection()
            if category_id:
                variable = RNVariable()
                df = self.select_to_dataframe(GET_INVESTED_CATEGORY, category_id)
                df['usdbrl'] = float(variable.get_variable('usd_dca'))
                df['amount'] = df.apply(lambda row: row['amount'] * row['usdbrl'] if row['is_usd'] == 1 else row['amount'], axis=1)
            else:
                df = self.select_to_dataframe(GET_ALL_CAPITAL_INJ)

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while getting capital injection:", str(e))

        finally:
            self.close_connection()

        return df