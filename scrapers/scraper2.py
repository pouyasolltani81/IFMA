import requests
from bs4 import BeautifulSoup

def scrape_news_topic_2():
    url = "https://example.com/news-topic-2"  # Replace with your target URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    news = []

    for item in soup.select('.article'):
        title = item.select_one('.headline').text.strip()
        description = item.select_one('.intro').text.strip()
        link = item.select_one('a')['href']
        tag = "Topic 2"
        summary = "Another brief summary."

        news.append({
            "title": title,
            "description": description,
            "link": link,
            "tag": tag,
            "summary": summary,
        })

    return news
