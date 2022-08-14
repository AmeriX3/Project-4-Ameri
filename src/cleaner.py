import sqlalchemy as alch
import os
import dotenv
import pandas as pd
dotenv.load_dotenv()
import plotly.express as px
import requests
from src import cleaner
passw = os.getenv("pass_sql")
dbName = "amazon_reviews"
connectionData = f"mysql+pymysql://root:password@localhost/amazon"
engine = alch.create_engine(connectionData)


def req_reviews():
    """
    Requests only the reviews and the votes
    """
    request = requests.get("http://127.0.0.1:5000/data/reviews").json()
    return request

def req_everything():
    """
    Requests all the data
    """
    request = requests.get("http://127.0.0.1:5000/data").json()
    
    return request