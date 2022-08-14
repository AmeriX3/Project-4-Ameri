from flask import Flask , jsonify
import json
from platform import java_ver
from config.sql_config import engine
import pandas as pd
import re
import spacy
import nltk 
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nlp = spacy.load("en_core_web_sm")
nlp.max_length= 1223510
sia = SentimentIntensityAnalyzer()
## GET
def get_everything ():

    query = (f"""
select * from amazon_reviews
order by  reviewTime desc;""")
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient="records")

def get_reviews():
    query = (f"""SELECT reviewText,helpful_yes,total_vote,reviewTime 
    FROM amazon_reviews 
    order by reviewTime desc;""")
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient="records")
def get_SpY(year):
    query = (f"""SELECT * 
    FROM amazon_reviews
    where reviewTime={year} 
    order by reviewTime desc;""")
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient="records")

def get_y(year):
    if year=="all":
        query = (f"""
        select * from amazon_reviews
        order by  reviewTime desc;""")
        df=pd.read_sql_query(query,con=engine)
        return df

    else:
        query = (f"""SELECT * 
        FROM amazon_reviews
        where reviewTime={year} 
        order by reviewTime desc;""")
        df=pd.read_sql_query(query,con=engine)
        return df

# Sentiment analyizer
def sa (x):
    try:
        return sia.polarity_scores(x)
    except:
        return x

