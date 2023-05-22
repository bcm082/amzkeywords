import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    unique_keywords = None
    df = pd.read_csv('Search_Terms_2023.csv')

    if request.method == "POST":
        searched_keyword = request.form["search"].lower()
        df = df[df['Search Term'].str.contains(searched_keyword, na=False)]
        unique_words = set()
        for term in df['Search Term'].unique():
            for word in term.split():
                unique_words.add(word.lower())
        unique_keywords = '\n'.join(sorted(list(unique_words)))
        return render_template("index.html", dataframe=df.head(50).to_html(classes="table table-striped", index=False), unique_keywords=unique_keywords)
        
    return render_template("index.html", dataframe=df.head(20).to_html(classes="table table-striped", index=False), unique_keywords=None)

if __name__ == "__main__":
    app.run(debug=True)



