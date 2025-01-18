import telebot
import schedule
import time
from googletrans import Translator
from scrapers.scraper1 import scrape_news_topic_1
from scrapers.scraper2 import scrape_news_topic_2

# Config
BOT_TOKEN = '7626220362:AAHP1a0zWjLRdmpzqfnbf2iXPd1iX538alI'
bot = telebot.TeleBot(BOT_TOKEN)
translator = Translator()

# Groups configuration
GROUPS = {
    "group_1": {'id': '-1002225374157', 'topic': 'Topic 1'},
    "group_2": {'id': 'CHAT_ID_2', 'topic': 'Topic 2'},
}




@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id  # Get the chat ID (group or user)
    chat_title = message.chat.title if message.chat.type != 'private' else "Private Chat"

    response = (
        f"Hello! 👋\n"
        f"Your Chat ID is: `{chat_id}`\n"
        f"Chat Name: {chat_title}\n"
        f"Type: {message.chat.type}"
    )
    bot.reply_to(message, response, parse_mode="Markdown")

    # Optionally, log or send this information to the bot admin
    admin_id = 166946747  # Replace with your Telegram ID
    bot.send_message(
        admin_id,
        f"Bot started in:\n"
        f"Chat ID: {chat_id}\n"
        f"Chat Name: {chat_title}\n"
        f"Type: {message.chat.type}",
    )


@bot.message_handler(commands=['get_my_id'])
def get_my_id(message):
    user_id = message.from_user.id
    bot.reply_to(message, f"Your Telegram ID is: `{user_id}`", parse_mode="Markdown")




# Function to format messages
def format_message(news_item):
    title = news_item['title']
    description = news_item['description']
    tag = news_item['tag']
    summary = news_item['summary']
    url = news_item['url']

    return (
        f"📢 *{title}*\n\n"
        f"📝 {description}\n\n"
        f"🏷️ Tag: {tag}\n\n"
        f"🔍 Summary: {summary}\n\n"
        f"{url}"
    )

# Send messages to specified group
def post_news_to_group(group_key, news_items):
    group = GROUPS[group_key]
    group_id = group['id']
    for news_item in news_items:
        formatted_message = format_message(news_item)
        translated_message = translator.translate(formatted_message, src='auto', dest='fa').text
        bot.send_message(group_id, translated_message, parse_mode='Markdown')

# Command to get group IDs
@bot.message_handler(commands=['get_groups'])
def get_groups(message):
    response = "\n".join([f"{key}: {value['id']}" for key, value in GROUPS.items()])
    bot.reply_to(message, f"Group IDs:\n{response}")

# Jobs for different groups
def job_group_1():
    news = scrape_news_topic_1()
    post_news_to_group('group_1', news)

def job_group_2():
    news = scrape_news_topic_2()
    post_news_to_group('group_2', news)

# Schedule jobs
# schedule.every(1).hour.do(job_group_1)  # Every hour
schedule.every(5).minutes.do(job_group_1) 
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
