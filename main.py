from flask import Flask , jsonify,request
import pandas as pd
import tools.sql_tools as sql
import json
import markdown.extensions.fenced_code
import re 
import plotly.express as px

app = Flask(__name__)

# Main page with the Readme
@app.route("/")
def index():
    readme_file = open("README.md", "r")
    md_template = markdown.markdown(readme_file.read(), extensions = ["fenced_code"])
    return md_template

# Route to recieve all Data   
@app.route("/data")
def all_lines ():
    return jsonify(sql.get_everything())

# Route to recieve only the reviews of the data
@app.route("/data/reviews")
def all_reviews():
    return jsonify(sql.get_reviews())

# Route to recieve Data from a specified year 
@app.route("/data/<year>")
def data_year(year):
    if year=="all":
        return jsonify(sql.get_everything())
    else:
        return jsonify(sql.get_SpY(year))

@app.route("/data/<year>/sa")
def data_SA(year):
    df= sql.get_y(year)
    df = pd.DataFrame.from_dict(df)
    alist = df["reviewText"].apply(sql.sa)
    lis=[]
    for i in alist:
        lis.append(i["compound"])
    df["sentiment_score"]= lis
    info = df.to_json()
    return info
  
@app.route("/post",methods=["POST"])
def insert_data():
    name = request.form.get("name")
    review = request.form.get("review")
    
    return sql.post_data(name,review)


if __name__ == '__main__':
    app.run(debug=True)
