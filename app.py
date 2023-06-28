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

def filter_keywords(keywords, limit=220):
    output = ''
    for keyword in keywords:
        if any(char.isdigit() for char in keyword):  # skip if keyword contains any digit
            continue
        if len(output) + len(keyword) + 1 > limit:  # +1 for space character
            break
        output += keyword + ' '
    return output


@app.route("/", methods=["GET", "POST"])
def index():
    unique_keywords = None
    df = pd.read_sql_table('SearchTerm', con=engine)

    if request.method == "POST":
        searched_keyword = request.form["search"].lower()
        filtered_df = df[df['SearchTerm'].str.contains(searched_keyword, na=False)]

        keyword_ranks = {}  # Store the unique keywords with their corresponding minimal rank

        for index, row in filtered_df.iterrows():
            for word in row['SearchTerm'].split():
                word = word.lower()
                if word not in keyword_ranks:
                    keyword_ranks[word] = row['SearchFrequencyRank']
                else:
                    keyword_ranks[word] = min(keyword_ranks[word], row['SearchFrequencyRank'])

        # Sort keywords by rank and then filter
        sorted_keywords = sorted(keyword_ranks, key=keyword_ranks.get)
        unique_keywords = filter_keywords(sorted_keywords)


        filtered_df = filtered_df.drop('id', axis=1)  # Drop the 'id' column from the DataFrame
        return render_template("index.html", dataframe=filtered_df.head(300).to_html(classes="table table-striped", index=False), unique_keywords=unique_keywords)

            
    df = df.drop('id', axis=1)  # Drop the 'id' column from the DataFrame
    return render_template("index.html", dataframe=df.head(20).to_html(classes="table table-striped", index=False), unique_keywords=None)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)