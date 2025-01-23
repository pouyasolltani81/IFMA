import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_news_topic_3():
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    base_url = "https://www.dailyforex.com/forex-technical-analysis/page-1"
    response = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the first news article link
    first_article = soup.select_one("div.top-info a")
    if not first_article:
        print("No articles found on the main page.")
        return []

    link = first_article['href']
    article_url = link if link.startswith("http") else urljoin(base_url, link)

    # Fetch the article page
    article_response = requests.get(article_url, headers=headers)
    article_soup = BeautifulSoup(article_response.text, 'html.parser')

    # Extract title
    title_element = article_soup.select_one("div.content-column h1")
    title = title_element.text.strip() if title_element else "Title not found"

    # Extract description
    description_element = article_soup.find("ul")
    description = description_element.text.strip() if description_element else "Description not found"

    # Extract tags (example: forex-related tags)
    tag_element = article_soup.select_one("div.tags")
    tag = tag_element.text.strip() if tag_element else "Tag not found"

    # Create a summary (if required, this can be more dynamic)
    summary = "This is a brief summary of the article."

    # Prepare the news data
    news = [{
        "title": title,
        "description": description,
        "link": article_url,
        "tag": tag,
        "summary": summary,
        "source": "Forex Live"
    }]

    return news


# Example usage
if __name__ == "__main__":
    scraped_news = scrape_news_topic_3()
    for article in scraped_news:
        print(article)
