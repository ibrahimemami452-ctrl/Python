import telebot
import threading
import queue
import sqlite3
import time

# Initialize the bot with your token
API_TOKEN = 'YOUR_API_TOKEN_HERE'
bot = telebot.TeleBot(API_TOKEN)

# Create a SQLite database for storing button states
connection = sqlite3.connect('button_states.db')
cursor = connection.cursor()

# Create a table to store button states
cursor.execute('''CREATE TABLE IF NOT EXISTS buttons (id INTEGER PRIMARY KEY, state TEXT)''')
connection.commit()

# Button handler
@bot.callback_query_handler(func=lambda call: True)
def handle_button(call):
    button_id = call.data
    # Update the state in the database
    cursor.execute('''INSERT OR REPLACE INTO buttons (id, state) VALUES (?, ?)''', (button_id, 'pressed'))
    connection.commit()
    bot.send_message(call.message.chat.id, f'Button {button_id} pressed!')

# Worker thread function to process updates
def worker_thread(q):
    while True:
        button_id = q.get()
        if button_id is None:
            break
        # Process the button press
        threading.Thread(target=lambda: handle_button(button_id)).start()
        q.task_done()

# Initialize the queue and start worker threads
q = queue.Queue()
num_worker_threads = 4
for _ in range(num_worker_threads):
    threading.Thread(target=worker_thread, args=(q,), daemon=True).start()

# Long polling to process messages
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f'Error: {e}')
        time.sleep(5)
