import telebot
import os
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = os.getenv("API_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def send_start_message(message):
    welcome_text = (
        "<b>Welcome to the DEXProxima VIP Signals Bot!</b>\n\n"
        "To gain <b>free lifetime access</b> to DEXProxima VIP:\n\n"
        "1 - Join ByBit using the button below\n"
        "2 - Deposit $100\n"
        "3 - Send your UID after this message!"
    )

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Join ByBit", url="https://www.bybit.com/invite?ref=7MZ63O4"))

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_info = f"User: @{message.from_user.username or 'NoUsername'}\nUID: {message.text}\n"
    bot.send_message(ADMIN_ID, f"New UID received:\n{user_info}")
    with open("uid_list.txt", "a") as f:
        f.write(user_info + "\n")
    bot.send_message(message.chat.id, "Thank you! Your UID has been received and is under review.")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Thank you! Your image has been received and is under review.")

bot.infinity_polling()