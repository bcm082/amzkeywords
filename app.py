from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SearchTerm.db'
db = SQLAlchemy(app)

engine = create_engine('sqlite:///SearchTerm.db', echo=True)

class SearchTerm(db.Model):
    __tablename__ = 'SearchTerm'
    id = db.Column(db.Integer, primary_key=True)
    SearchTerm = db.Column(db.String(500), nullable=False)
    SearchFrequencyRank = db.Column(db.Integer, nullable=False)

@app.route("/", methods=["GET", "POST"])
def index():
    unique_keywords = None
    df = pd.read_sql_table('SearchTerm', con=engine)

    if request.method == "POST":
        searched_keyword = request.form["search"].lower()
        df = df[df['SearchTerm'].str.contains(searched_keyword, na=False)]
        unique_words = set()
        for SearchTerm in df['SearchTerm'].unique():
            for word in SearchTerm.split():
                unique_words.add(word.lower())
        unique_keywords = '\n'.join(sorted(list(unique_words)))
        df = df.drop('id', axis=1)
        return render_template("index.html", dataframe=df.head(300).to_html(classes="table table-striped", index=False), unique_keywords=unique_keywords)
    
    df = df.drop('id', axis=1)
    return render_template("index.html", dataframe=df.head(20).to_html(classes="table table-striped", index=False), unique_keywords=None)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)



