import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from itertools import cycle
import time



def scrape_news_topic_8():
    # --- Configuration ---

    # Advanced headers mimicking a real browser
    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/115.0.0.0 Safari/537.36'),
        'Accept': ('text/html,application/xhtml+xml,application/xml;'
                'q=0.9,image/webp,*/*;q=0.8'),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.google.com/',
        'Connection': 'keep-alive'
    }

    # Optional: List of proxy endpoints (format: "http://user:pass@ip:port")
    PROXIES_LIST = [
        # Example proxies—replace with your own or leave empty to not use proxies.
        # "http://username:password@proxy1.example.com:3128",
        # "http://username:password@proxy2.example.com:3128",
    ]

    # Create a cycle iterator if proxies are provided
    proxies_cycle = cycle(PROXIES_LIST) if PROXIES_LIST else None


    # Retry configuration
    MAX_RETRIES = 5
    DELAY_SECONDS = 2

# URL to fetch

    base_url = "https://cryptopotato.com"
    url = f"{base_url}/crypto-news"

    try:

        # Optionally update proxies for each request
        session = requests.Session()
        session.headers.update(HEADERS)
       
        response = session.get(url, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (e.g. 40
        
        print('maaaaaadaaareto :')
        print(response)
        # # Fetch the main news page
        # response = requests.get(url, headers=headers)
      
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
            "tag": 'crypto_tag',
            "source": "CryptoPotato",
            "link": article_url
        }]

        # # Print the news
        # for article in news:
        #     print(f"Title: {article['title']}")
        #     print(f"Descriptions: {', '.join(article['description'])}")
        #     print(f"Source: {article['source']}")
        #     print(f"Tags: {', '.join(article['tag'])}")
        #     print(f"Link: {article['link']}")

        print(news)

        return news

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
