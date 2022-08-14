from flask import Flask , jsonify
import pandas as pd
import tools.sql_tools as sql
import json
import markdown.extensions.fenced_code
import re 
import plotly.express as px
app = Flask(__name__)

@app.route("/")
def index():
    readme_file = open("README.md", "r")
    md_template = markdown.markdown(readme_file.read(), extensions = ["fenced_code"])
    return md_template
@app.route("/data")
def all_lines ():
    return jsonify(sql.get_everything())
    
@app.route("/data/reviews")
def all_reviews():
    return jsonify(sql.get_reviews())

@app.route("/data/<year>")
def data_year(year):
    if year=="all":
        return jsonify(sql.get_everything())
    else:
        return jsonify(sql.get_SpY(year))

@app.route("/data/<year>/sa")
def data_SA(year):
    df= sql.get_y(year)
    alist = df["reviewText"].apply(sql.sa)
    lis=[]
    for i in alist:
        lis.append(i["compound"])
    df["sentiment_score"]= lis
    info = df.to_json()
    return info
  



if __name__ == '__main__':
    app.run(debug=True)