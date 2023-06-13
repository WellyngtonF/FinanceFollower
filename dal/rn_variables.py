import pandas as pd

from dal.rn_base import RNBase

GET_VARIABLE = """
    SELECT value
    FROM global_variables
    WHERE description = :param1
"""

class RNVariable(RNBase):    

    def get_variable(self, variable: str) -> pd.DataFrame:
        try:
            self.create_connection()
            df = self.select_to_dataframe(GET_VARIABLE, variable)
            value = df['value'][0]

        except Exception as e:
            value = None
            print("Error occurred while selecting a global variable:", str(e))

        finally:
            self.close_connection()

        return value