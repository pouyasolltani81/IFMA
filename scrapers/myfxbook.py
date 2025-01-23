from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def scrape_news_topic_2():
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)
    time.sleep(1)

    # Open the website
    driver.get('https://www.myfxbook.com/news')
    wait = WebDriverWait(driver, 10)

    # Click on initial buttons
    try:
        click1 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "cky-btn-accept")))
        click1.click()
        time.sleep(1)  # Adding a small delay to ensure the first click is processed
        click2 = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "news-top-title")))
        click2.click()
    except Exception as e:
        print(f"Error clicking on buttons: {e}")

    # Find and click on the first news link
    try:
        link = driver.find_element(By.CSS_SELECTOR, "h2.news-top-title a")
        link.click()  # Click on the first link
        print("Click on the link was successful.")
    except Exception as e:
        print(f"Error clicking on the news link: {e}")

    # Extract news data
    try:
        # Find the news title
        try:
            title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.col-xs-12 h1"))).text
        except:
            title = "Title not found"

        # Find the news content
        p_elements = driver.find_elements(By.TAG_NAME, 'p')

        # Extract paragraph text
        paragraph_text = " ".join([p.text for p in p_elements])

        forex_tag = [
            "#فارکس", "#اخبار_فارکس", "#اخبار_اقتصادی", "#اخبار_دلار", "#اخبار_جهانی",
            "#بازار_مالی", "#signal", "#SIGNALFOREX", "#forex", "#news", "#tahlil",
            "#تحلیل", "#تکنیکال", "#فاندامنتال"
        ]
        # Append the news data to the list
        news_with_additional_info = []
        news_with_additional_info.append({
            "title": title,
            "description": paragraph_text,
            "link": driver.current_url,  # Current URL after clicking the news link
            "tag": forex_tag,  # You can replace with actual tag if available
            "source": 'myfxbook'
        })

        for news in news_with_additional_info:
           
                
            # Close WebDriver
           driver.quit()
                
           return news

    except Exception as e:
        print(f"Error extracting news data: {e}")
