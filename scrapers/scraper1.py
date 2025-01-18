import requests
from bs4 import BeautifulSoup



def scrape_news_topic_1():
    headers  =  { 'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
    url = "https://www.forexlive.com/"
    response = requests.get(url ,  headers= headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all("div", class_="article-list__item-wrapper")
    link = articles[0].find("a")["href"]
    article_url = link if link.startswith("http") else url + link
    response = requests.get(article_url ,  headers= headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    tag = soup.find("a", class_="article-header__category-section") 


    
    title = soup.find("h3", class_="article-slot__title").text.strip()
    print(title)
    description = soup.find("article", class_='article__content-body').find_all("p")[0].text.strip()
    # author = soup.find("span", class_="auth-name").text.strip()
    # publish_date = soup.find("div", class_="publisher-details__date").text.strip()
    
    # img_thum = img_thum_div.find("img")["src"] if img_thum_div else Non
    # main = soup.find("div", class_="article-body")
    # imgs = [img["src"] for img in main.find_all("img")
    # tags = [tag.text.strip() for tag in soup.find_all("a", rel="tag")]
    # content = main.text.strip()
    # scraped_date = datetime.now()
    news = []
    print('works')

    
    # title = 'srgsdrgf'
    # description = 'sevec'
    # link = 'wer'
    # tag = "Topic 1"
    summary = "Short summary about the news."

    news.append({
        "title": title,
        "description": description,
        "link": link,
        "tag": tag,
        "summary": summary,
        
    })

    return news
