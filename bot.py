import sqlite3
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = '7630363248:AAELdZB7RKILflny_pzm28qxJdld8dieQsc'

# Initialize the database
conn = sqlite3.connect('manike_bot.db', check_same_thread=False)
c = conn.cursor()

# Create tables if they don't exist
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    referral_id INTEGER,
    points INTEGER DEFAULT 0
)
''')

def start(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    referral_id = int(context.args[0]) if context.args else None

    # Add the user to the database
    c.execute('INSERT OR IGNORE INTO users (user_id, referral_id) VALUES (?, ?)', (user_id, referral_id))
    conn.commit()

    if referral_id:
        # Reward the referrer
        c.execute('UPDATE users SET points = points + 10 WHERE user_id = ?', (referral_id,))
        conn.commit()

    # Generate referral link
    referral_link = f"https://t.me/ManikeBot?start={user_id}"
    update.message.reply_text(f"Welcome to Manike! Your referral link: {referral_link}")

def points(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    c.execute('SELECT points FROM users WHERE user_id = ?', (user_id,))
    points = c.fetchone()
    points = points[0] if points else 0
    update.message.reply_text(f"You have {points} Manike Points.")

# Set up the bot
updater = Updater(BOT_TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('points', points))

# Start polling for updates
updater.start_polling()
updater.idle()
