import requests
from newspaper import Article
from transformers import pipeline

# Replace with your NewsAPI API key
API_KEY = '4cc0831599914e1482792460435acb36'
BASE_URL = 'https://newsapi.org/v2/top-headlines'

# Initialize the summarization model
summarizer = pipeline("summarization")

def fetch_news(country='in'):
    params = {
        'country': country,
        'apiKey': API_KEY,
        'pageSize': 5  # Number of articles to fetch
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()['articles']
    else:
        print(f"Error: {response.status_code}, {response.json().get('message', 'No message')}")
        return []

def summarize_article(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    return article.title, article.text

def create_one_liner(summary):
    # Summarize only if content is sufficient
    if len(summary.split()) > 10:
        return summarizer(summary, max_length=30, min_length=10, do_sample=False)[0]['summary_text']
    else:
        return summary  # Return the original text if too short

def main():
    articles = fetch_news()

    if not articles:
        print("No articles found.")
        return

    for article in articles:
        title, content = summarize_article(article['url'])
        one_liner = create_one_liner(content)

        print(f"Title: {title}")
        print(f"One-liner Breaking News: {one_liner}\n")

if __name__ == '__main__':
    main()
