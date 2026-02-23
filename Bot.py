import telebot
import sqlite3
from telebot import types
import threading

# Database setup
conn = sqlite3.connect('bot_database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS commands (id INTEGER PRIMARY KEY, command TEXT)''')
conn.commit()

API_TOKEN = 'YOUR_TELEGRAM_BOT_API_TOKEN'

bot = telebot.TeleBot(API_TOKEN)

# Function to handle dashboard button
@bot.message_handler(func=lambda message: message.text == 'Dashboard')
def handle_dashboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Button 1')
    item2 = types.KeyboardButton('Button 2')
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Choose an option:', reply_markup=markup)

# Function to handle long polling
def start_polling():
    bot.polling(none_stop=True)

# Worker thread to handle polling
threads = []
for i in range(10):
    thread = threading.Thread(target=start_polling)
    thread.start()
    threads.append(thread)

# Function to handle button 1
@bot.message_handler(func=lambda message: message.text == 'Button 1')
def handle_button1(message):
    bot.send_message(message.chat.id, 'You pressed Button 1!')

# Function to handle button 2
@bot.message_handler(func=lambda message: message.text == 'Button 2')
def handle_button2(message):
    bot.send_message(message.chat.id, 'You pressed Button 2!')

# Handle commands
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Welcome! Click the button below to enter the dashboard:', reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(types.KeyboardButton('Dashboard')))

# Main execution
if __name__ == '__main__':
    start_polling()  
