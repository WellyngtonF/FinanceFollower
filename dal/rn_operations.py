import pandas as pd
from datetime import datetime

from dal.rn_base import RNBase
from dal.rn_variables import RNVariable

INSERT_OPERATION = """
    INSERT INTO operations (idasset, date_operation, quantity, price, direction, insert_date, update_date)
    VALUES (:param1, :param2, :param3, :param4, :param5, :param6, :param7)
"""

GET_MINIMAL_DATE = """
    SELECT MIN(date_operation) date
    FROM operations
"""

GET_OPERATIONS_BY_DATA_RANGE = """
    SELECT A.description Ativo, C.description Categoria, O.date_operation Data, O.quantity Quantidade, O.price "Preço (R$)", O.quantity * O.price "Total (R$)", IF(direction = 1, "Compra", "Venda") "Operação", A.is_usd, A.idcategory
    FROM operations O
    INNER JOIN Asset A ON A.idasset = O.idasset
    INNER JOIN Category C ON C.idcategory = A.idcategory
    WHERE O.date_operation >= :param1
        AND O.date_operation <= :param2
"""

class RNOperation(RNBase):    
    def insert_operation(self, asset_id, date_operation, quantity, price, direction) -> None:
        # Get the current datetime
        current_datetime = datetime.now()

        data = [asset_id, date_operation, quantity, price, direction, current_datetime, current_datetime]

        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            self.execute_script(INSERT_OPERATION, data)

        except Exception as e:
            # Handle any errors that occur during the insertion process
            print("Error occurred while inserting operation:", str(e))

        finally:
            # Close the database connection
            self.close_connection()

    def get_minimal_operational_date(self) -> datetime:
        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            df = self.select_to_dataframe(GET_MINIMAL_DATE)

            date = df['date'][0]

        except Exception as e:
            date = None
            print("Error occurred while getting minimal date:", str(e))

        finally:
            # Close the database connection
            self.close_connection()
        
        return date
    
    def get_operations(self, min_date: str, max_date:str, category_id: str, asset: str) -> pd.DataFrame:
        try:
            # Establish a database connection
            self.create_connection()

            data = [min_date, max_date]

            # Execute the SQL query with the data
            df = self.select_to_dataframe(GET_OPERATIONS_BY_DATA_RANGE, data)

            if category_id != None:
                df = df[df['idcategory'] == category_id]

            if asset != '':
                df = df[df['Ativo'].str.contains(asset, case=False)]

            df = df.sort_values('Data')

            variable = RNVariable()
            df['usdbrl'] = float(variable.get_variable('usd_dca'))
            df['Preço (R$)'] = df.apply(lambda row: row['Preço (R$)'] * row['usdbrl'] if row['is_usd'] == 1 else row['Preço (R$)'], axis=1)
            df['Total (R$)'] = df['Preço (R$)'] * df['Quantidade']

            # Formatação DF
            df['Data'] = df['Data'].dt.strftime('%d/%m/%Y')

            df = df[['Ativo', 'Categoria', 'Data', 'Quantidade', 'Preço (R$)', 'Total (R$)', 'Operação']]

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while getting operation:", str(e))

        finally:
            # Close the database connection
            self.close_connection()
        
        return df