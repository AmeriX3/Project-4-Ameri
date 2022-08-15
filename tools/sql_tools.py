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

# Get all Data
def get_everything ():

    query = (f"""
select reviewerName, reviewText,reviewTime from amazon_reviews
order by  reviewTime desc;""")
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient="records")


#Get only the reviews
def get_reviews():
    query = (f"""SELECT reviewText 
    FROM amazon_reviews 
    order by reviewTime desc;""")
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient="records")

# Get a specified year
def get_SpY(year):
    query = (f"""SELECT reviewerName, reviewText,reviewTime 
    FROM amazon_reviews
    where reviewTime={year} 
    order by reviewTime desc;""")
    df=pd.read_sql_query(query,con=engine)
    return df.to_dict(orient="records")

# Get a specified year (for a different function)
def get_y(year):
    if year=="all":
        query = (f"""
        select reviewerName, reviewText, reviewTime 
        from amazon_reviews
        order by  reviewTime desc;""")
        df=pd.read_sql_query(query,con=engine)
        return df.to_dict(orient="records")

    else:
        query = (f"""SELECT reviewerName, reviewText, reviewTime
        FROM amazon_reviews
        where reviewTime={year} 
        order by reviewTime desc;""")
        df=pd.read_sql_query(query,con=engine)
        return df.to_dict(orient="records")

# Sentiment analyizer
def sa (x):
    try:
        return sia.polarity_scores(x)
    except:
        return x

# Posting function
def post_data (name, review):
    query="""
    select CURDATE();
    """
    date=pd.read_sql_query(query,con=engine)
    date= date.to_dict()
    date= date["CURDATE()"][0]
    
    engine.execute(f"""
    INSERT INTO amazon_reviews (reviewerName, reviewText,reviewTime) VALUES ("{name}", "{review}","{date}");
    """)
    
    return f"{name},{review},{date} Has been added"