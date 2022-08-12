from flask import Flask , jsonify
import random
import tools.sql_tools as sql
import json
import markdown.extensions.fenced_code
app = Flask(__name__)

@app.route("/")
def index():
    readme_file = open("README.md", "r")
    md_template = markdown.markdown(readme_file.read(), extensions = ["fenced_code"])
    return md_template
@app.route("/data")
def all_lines ():
    return jsonify(sql.get_everything())


if __name__ == '__main__':
    app.run()