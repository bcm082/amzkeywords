import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        searched_keyword = request.form["search"].lower()
        df = pd.read_csv("SearchTerms_2022.csv")
        df = df[df["Search Term"].str.contains(searched_keyword, na=False, case=False)]
        return render_template("index.html", dataframe=df.head(50).to_html(classes="table table-striped", index=False))
    return render_template("index.html", dataframe=None)

if __name__ == "__main__":
    app.run(debug=True)

