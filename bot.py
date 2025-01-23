import telebot
import schedule
import time
import requests
from googletrans import Translator
from scrapers.scraper1 import scrape_news_topic_1
from scrapers.scraper2 import scrape_news_topic_2

forex_live_latest_news = ['123443f1']

# Config
BOT_TOKEN = '7626220362:AAHP1a0zWjLRdmpzqfnbf2iXPd1iX538alI'
bot = telebot.TeleBot(BOT_TOKEN)
translator = Translator()

# Groups configuration
GROUPS = {
    "group_1": {'id': '-1002225374157', 'topic': 'Topic 1' , 'topic_id' : '396' },
    "group_2": {'id': 'CHAT_ID_2', 'topic': 'Topic 2'},
}



@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id  # Get the chat ID (group, channel, or user)
    chat_title = message.chat.title if message.chat.type != 'private' else "Private Chat"
    topic_id = message.message_thread_id if hasattr(message, 'message_thread_id') else None  # For forum topics

    # Check if the chat type is a channel
    if message.chat.type == 'channel':
        channel_id = chat_id
    else:
        channel_id = None

    # Construct the response message
    response = (
        f"Hello! 👋\n"
        f"Your Chat ID is: `{chat_id}`\n"
        f"Chat Name: {chat_title}\n"
        f"Type: {message.chat.type}\n"
    )
    if topic_id:
        response += f"Topic ID: `{topic_id}`\n"
    if channel_id:
        response += f"Channel ID: `{channel_id}`\n"

    bot.reply_to(message, response, parse_mode="Markdown")

    # Optionally, log or send this information to the bot admin
    admin_id = 166946747  # Replace with your Telegram ID
    admin_message = (
        f"Bot started in:\n"
        f"Chat ID: {chat_id}\n"
        f"Chat Name: {chat_title}\n"
        f"Type: {message.chat.type}\n"
    )
    if topic_id:
        admin_message += f"Topic ID: {topic_id}\n"
    if channel_id:
        admin_message += f"Channel ID: {channel_id}\n"

    bot.send_message(admin_id, admin_message)



@bot.message_handler(commands=['get_my_id'])
def get_my_id(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"Your Telegram ID is: `{user_id}`", parse_mode="Markdown")


def translate_text(text, target_language):
    url = "http://localhost:8000/translate"
    payload = {
        "text": text,
        "to": target_language
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json().get("translatedText", "Translation failed.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Error: {str(e)}"


# Function to format messages
# Function to format messages without translating the URL
def format_message(news_item):
    title = news_item['title']
    description = news_item['description']
    tag = news_item['tag']
    summary = news_item['summary']
    url = news_item['url']

    # Create a clickable Telegram link with custom text
    formatted_url = f"[Click here to view]({url})"  # Custom text for the link

    # Prepare the formatted message without the URL
    message = (
        f"📢 *{title}*\n\n"
        f"📝 {description}\n\n"
        f"🏷️ Tag: {tag}\n\n"
        # f"🔍 Summary: {summary}\n\n"
    )

    # Return both the text (for translation) and the URL separately
    return message, formatted_url

# Send messages to specified group
def post_news_to_group(group_key, news_items , source):

    
    new_news =True
    
    group = GROUPS[group_key]
    group_id = group['id']
    topic_id = group.get('topic_id')  # Retrieve the topic ID if present
    channel_id = group.get('channel_id')  # Retrieve the channel ID if present

    for news_item in news_items:
        # Format the message and get the URL separately
        formatted_message, url = format_message(news_item)

        if (source == 'forexlive'):
            forex_live_latest_news.append(url)
            if (forex_live_latest_news[-1] == forex_live_latest_news[0]):
                forex_live_latest_news.pop(0)
                new_news = False

        
        # Translate the message text (excluding the URL)
        translated_message = translate_text(formatted_message, "fa")
        
        # Add the URL at the end of the translated message
        final_message = f"{translated_message}\n\n{url}"
        
        print(f"Final Message: {final_message}")
        
        if (new_news) :

            
            # Determine the target destination
            if topic_id:
                bot.send_message(group_id, final_message, parse_mode='Markdown', message_thread_id=topic_id)
            elif channel_id:
                bot.send_message(channel_id, final_message, parse_mode='Markdown')
            else:
                bot.send_message(group_id, final_message, parse_mode='Markdown')


# Command to get group IDs
@bot.message_handler(commands=['get_groups'])
def get_groups(message):
    response = "\n".join([f"{key}: {value['id']}" for key, value in GROUPS.items()])
    bot.reply_to(message, f"Group IDs:\n{response}")

# Jobs for different groups
def job_group_1():
    news = scrape_news_topic_1()
    post_news_to_group('group_1', news , 'forexlive')

def job_group_2():
    news = scrape_news_topic_2()
    post_news_to_group('group_2', news)

# Schedule jobs
# schedule.every(1).hour.do(job_group_1)  # Every hour
# schedule.every(5).minutes.do(job_group_1) 
schedule.every(5).seconds.do(job_group_1) 


# Run the scheduler in a separate thread
def run_scheduler():
    print('Scheduler runner is getting started')
    while True:
        print('Scheduler runner started')
        schedule.run_pending()
        time.sleep(1)

# Start scheduler thread
import threading
scheduler_thread = threading.Thread(target=run_scheduler)
scheduler_thread.start()

# Start the bot
bot.polling()
