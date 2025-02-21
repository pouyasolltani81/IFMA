import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from itertools import cycle
import time

def get_free_proxies():
    """
    Fetch free proxies from free-proxy-list.net and sslproxies.org.
    Returns a list of proxies in the format "http://ip:port" that are elite and support HTTPS.
    """
    proxy_sources = [
        "https://free-proxy-list.net/",
        "https://www.sslproxies.org/"
    ]
    HEADERS = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/115.0.0.0 Safari/537.36'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    proxies = []
    for source in proxy_sources:
        try:
            print(f"Fetching proxies from {source}")
            response = requests.get(source, headers=HEADERS, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            proxy_table = soup.find("table", id="proxylisttable")
            if proxy_table and proxy_table.tbody:
                for row in proxy_table.tbody.find_all("tr"):
                    cols = row.find_all("td")
                    if len(cols) >= 7:
                        ip = cols[0].text.strip()
                        port = cols[1].text.strip()
                        anonymity = cols[4].text.strip()  # e.g., "elite proxy"
                        https_support = cols[6].text.strip()  # "yes" or "no"
                        if anonymity.lower() == "elite proxy" and https_support.lower() == "yes":
                            proxies.append(f"http://{ip}:{port}")
            if proxies:
                print(f"Found {len(proxies)} proxies from {source}")
                return proxies
            else:
                print(f"No proxies found at {source}")
        except Exception as e:
            print(f"Error fetching proxies from {source}: {e}")
    return proxies

def scrape_news_topic_8():
    # --- Configuration ---
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

    # Automatically fetch the latest free elite HTTPS proxies
    proxies_list = get_free_proxies()
    if not proxies_list:
        print("No proxies fetched. Exiting.")
        return None
    print("Fetched proxies:", proxies_list)
    proxies_cycle = cycle(proxies_list)

    base_url = "https://cryptopotato.com"
    url = f"{base_url}/crypto-news"

    MAX_RETRIES = 5
    DELAY_SECONDS = 2

    session = requests.Session()
    session.headers.update(HEADERS)

    page_content = None
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            current_proxy = next(proxies_cycle)
            session.proxies.update({
                'http': current_proxy,
                'https': current_proxy,
            })
            print(f"Attempt {attempt}: Using proxy {current_proxy}")
            response = session.get(url, timeout=10)
            response.raise_for_status()
            print(f"Success on attempt {attempt}!")
            page_content = response.text
            break
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt} failed with error: {e}")
            time.sleep(DELAY_SECONDS)
    
    if page_content is None:
        print("All attempts failed. Could not fetch the page.")
        return None

    soup = BeautifulSoup(page_content, 'html.parser')
    first_news = soup.select_one("h3.rpwe-title a")
    if not first_news:
        print("No news link found.")
        return None

    link = first_news['href']
    article_url = link if link.startswith("http") else urljoin(base_url, link)

    try:
        news_response = session.get(article_url, timeout=10)
        news_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch news article page: {e}")
        return None

    news_soup = BeautifulSoup(news_response.text, 'html.parser')
    title_element = news_soup.select_one("div.page-title h1")
    title = title_element.text.strip() if title_element else "Title not found"
    p_tags = news_soup.find_all("p")
    descriptions = [p.text.strip() for p in p_tags]

    crypto_tag = [
        "#کریپتو", "#ارز_دیجیتال", "#بیت_کوین", "#اتریوم", "#سرمایه_گذاری",
        "#رمزارز", "#ترید", "#ماینینگ", "#تحلیل_بازار", "#بلاکچین",
        "#کریپتوکارنسی", "#ارزهای_دیجیتال", "#بازار_مالی", "#پول_دیجیتال",
        "#معاملات_ارز_دیجیتال", "#سرمایه_گذاری_آنلاین", "#اخبار_جهانی", "#سرمایه_گذاری_آنلاین"
    ]

    news = [{
        "title": title,
        "description": descriptions,
        "tag": 'crypto_tag',
        "source": "CryptoPotato",
        "link": "article_url"
    }]

    print(news)
    return news

if __name__ == "__main__":
    news = scrape_news_topic_8()
    if news:
        print(news)
