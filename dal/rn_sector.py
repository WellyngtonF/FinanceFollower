import pandas as pd
from datetime import datetime

from dal.rn_base import RNBase

GET_ALL_SECTORS = """
    SELECT S.idsector, C.description category_description, S.description
    FROM sector S
    INNER JOIN category C ON C.idcategory = S.idcategory
"""

INSERT_SECTOR = """
    INSERT INTO sector (idcategory, description, insert_date, update_date)
    VALUES (:param1, :param2, :param3, :param4)
"""

GET_SECTOR_FROM_ID = """
    SELECT idsector, idcategory, description
    FROM sector
    WHERE idsector = :param1
"""

GET_SECTOR_FROM_CATEGORY = """
    SELECT idsector, description
    FROM sector
    WHERE idcategory = :param1
"""

UPDATE_SECTOR = """
    UPDATE sector
    SET idcategory = :param1,
        description = :param2,
        update_date = :param3
    WHERE idsector = :param4
"""

DELETE_SECTOR = """
    DELETE FROM sector
    WHERE idsector = :param1
"""

column_mapping = {
    'idsector': 'id',
    'category_description': 'Categoria',
    'description': 'Setor',
}

class RNSector(RNBase):
    def modeling_column(self, df: pd.DataFrame) -> pd.DataFrame:
        renamed_df = df.rename(columns=column_mapping)

        return renamed_df
    
    def get_sectors(self) -> pd.DataFrame:
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_ALL_SECTORS)

            df = self.modeling_column(df)

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while selecting sector:", str(e))

        finally:
            self.close_connection()

        return df
    
    def insert_sector(self, idcategory, description) -> None:
        # Get the current datetime
        current_datetime = datetime.now()

        data = [idcategory, description, current_datetime, current_datetime]

        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            self.execute_script(INSERT_SECTOR, data)

        except Exception as e:
            # Handle any errors that occur during the insertion process
            print("Error occurred while inserting sector:", str(e))

        finally:
            # Close the database connection
            self.close_connection()

    def get_sector_by_id(self, sector_id) -> pd.DataFrame:
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_SECTOR_FROM_ID, sector_id)

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while updating sector:", str(e))

        finally:
            self.close_connection()

        return df
    
    def get_sector_by_idcategory(self, category_id) -> pd.DataFrame:
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_SECTOR_FROM_CATEGORY, category_id)

        except Exception as e:
            df = pd.DataFrame([])
            print("Error occurred while updating sector:", str(e))

        finally:
            self.close_connection()

        return df
            
    
    def edit_sector(self, category_id, description, sector_id) -> pd.DataFrame:

        current_datetime = datetime.now()

        data = [category_id, description, current_datetime, sector_id]

        try:
            # Establish a database connection
            self.create_connection()

            # Execute the SQL query with the data
            self.execute_script(UPDATE_SECTOR, data)

        except Exception as e:
            # Handle any errors that occur during the insertion process
            print("Error occurred while inserting sector:", str(e))

        finally:
            # Close the database connection
            self.close_connection()

    def delete_sector(self, sector_id) -> None:
        try:
            self.create_connection()
            self.execute_script(DELETE_SECTOR, sector_id)

        except Exception as e:
            print("Error occurred while deleting sector:", str(e))

        finally:
            self.close_connection()

    def have_sector(self, category_id: str) -> bool:
        try:
            self.create_connection()
            df = self.get_sector_by_idcategory(category_id)

            return len(df.index) > 0
        except Exception as e:
            print("Error occurred while verifying if category has sector:", str(e))
            return False

        finally:
            self.close_connection()
