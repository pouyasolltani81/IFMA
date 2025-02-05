import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def scrape_news_topic_8():
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    }
    base_url = "https://cryptopotato.com"
    url = f"{base_url}/crypto-news"

    try:
        # Fetch the main news page
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the first news article
        first_news = soup.select_one("h3.rpwe-title a")
        if not first_news:
            print("No news link found.")
            return None

        # Extract the link and fix if relative
        link = first_news['href']
        article_url = link if link.startswith("http") else urljoin(base_url, link)

        # Fetch the specific news article page
        news_response = requests.get(article_url, headers=headers)
        news_response.raise_for_status()
        news_soup = BeautifulSoup(news_response.text, 'html.parser')

        # Extract title
        title_element = news_soup.select_one("div.page-title h1")
        title = title_element.text.strip() if title_element else "Title not found"

        # Extract all <p> tags
        p_tags = news_soup.find_all("p")
        descriptions = [p.text.strip() for p in p_tags]

        crypto_tag = [
            "#کریپتو", "#ارز_دیجیتال", "#بیت_کوین", "#اتریوم", "#سرمایه_گذاری",
            "#رمزارز", "#ترید", "#ماینینگ", "#تحلیل_بازار", "#بلاکچین",
            "#کریپتوکارنسی", "#ارزهای_دیجیتال", "#بازار_مالی", "#پول_دیجیتال",
            "#معاملات_ارز_دیجیتال", "#سرمایه_گذاری_آنلاین", "#اخبار_جهانی", "#سرمایه_گذاری_آنلاین"
        ]

        # Prepare the news object
        news = [{
            "title": title,
            "description": descriptions,
            "tag": crypto_tag,
            "source": "CryptoPotato",
            "link": article_url
        }]

        # Print the news
        for article in news:
            print(f"Title: {article['title']}")
            print(f"Descriptions: {', '.join(article['description'])}")
            print(f"Source: {article['source']}")
            print(f"Tags: {', '.join(article['tag'])}")
            print(f"Link: {article['link']}")

    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    news = scrape_news_topic_8()
    if news:
        print(news)
