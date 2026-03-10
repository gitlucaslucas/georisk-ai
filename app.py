from flask import Flask, render_template
import requests
from textblob import TextBlob

app = Flask(__name__)

NEWS_API = "https://newsapi.org/v2/everything?q=war OR conflict OR military&language=en&apiKey=demo"

def analyze_news():
    try:
        r = requests.get(NEWS_API)
        data = r.json()

        results = []

        for article in data.get("articles", [])[:10]:
            title = article["title"]

            sentiment = TextBlob(title).sentiment.polarity

            if sentiment < -0.2:
                risk = "HIGH"
            elif sentiment < 0.1:
                risk = "MEDIUM"
            else:
                risk = "LOW"

            results.append({
                "title": title,
                "risk": risk
            })

        return results

    except:
        return []

@app.route("/")
def index():

    news = analyze_news()

    high = len([n for n in news if n["risk"] == "HIGH"])
    medium = len([n for n in news if n["risk"] == "MEDIUM"])
    low = len([n for n in news if n["risk"] == "LOW"])

    return render_template(
        "index.html",
        news=news,
        high=high,
        medium=medium,
        low=low
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
