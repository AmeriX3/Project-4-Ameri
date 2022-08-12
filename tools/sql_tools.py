from config.sql_config import engine
import pandas as pd

## GET
def get_everything ():

    query = (f"""SELECT *FROM amazon_reviews;""")
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict()
