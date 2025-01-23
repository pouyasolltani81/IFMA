import requests
from bs4 import BeautifulSoup

def scrape_news_topic_2():
    url = 'https://www.myfxbook.com/news'

    try:
        # Send a GET request to fetch the page content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes

        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find and extract the first news link
        first_news = soup.select_one("h2.news-top-title a")
        if not first_news:
            print("No news link found.")
            return None

        news_url = first_news['href']  # Get the href attribute (link)

        # Fetch the specific news page
        news_response = requests.get(news_url)
        news_response.raise_for_status()
        news_soup = BeautifulSoup(news_response.content, 'html.parser')

        # Extract the news title
        title_element = news_soup.select_one("div.col-xs-12 h1")
        title = title_element.text.strip() if title_element else "Title not found"

        # Extract all paragraphs
        paragraphs = news_soup.find_all('p')
        paragraph_text = " ".join([p.text.strip() for p in paragraphs])

        # Tags for the news
        forex_tags = [
            "#فارکس", "#اخبار_فارکس", "#اخبار_اقتصادی", "#اخبار_دلار", "#اخبار_جهانی",
            "#بازار_مالی", "#signal", "#SIGNALFOREX", "#forex", "#news", "#tahlil",
            "#تحلیل", "#تکنیکال", "#فاندامنتال"
        ]

        # Create a dictionary for the extracted data
        news_data = {
            "title": title,
            "description": paragraph_text,
            "link": news_url,
            "tag": 'forex_tags',
            "source": 'myfxbook'
        }

        return news_data

    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":
    news = scrape_news_topic_2()
    if news:
        print(news)
