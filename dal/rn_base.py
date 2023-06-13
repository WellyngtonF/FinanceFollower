from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

class RNBase:
    def __init__(self) -> None:
        load_dotenv()
        self.db_user = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_host = os.getenv("HOST")
        self.db_name = os.getenv("DATABASE")
        self.connection = None

    def create_connection(self) -> None:
        # Create the database URL
        db_url = f'mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'

        # Create the engine and connect to the database
        self.connection = create_engine(db_url).connect()

    def close_connection(self) -> None:
        if self.connection:
            self.connection.close()

    def execute_script(self, query, data:any=[]) -> any:
        params =[]
        if data != []:
            if isinstance(data, list):
                params = {f"param{i+1}": value for i, value in enumerate(data)}
            else:
                params = {'param1': data}

        result = self.connection.execute(text(query), params)
        self.connection.commit()
        return result
    
    def select_to_dataframe(self, query, data=[]) -> pd.DataFrame:
        # Execute the SELECT query and fetch the results
        result = self.execute_script(query, data)
        data = result.fetchall()

        # Convert the results to a Pandas DataFrame
        columns = result.keys()
        df = pd.DataFrame(data, columns=columns)

        return df
    
    def dataframe_to_db(self, df: pd.DataFrame, table: str):
        df.to_sql(table, self.connection.engine, if_exists='append', index=False)