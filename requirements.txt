import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = '8041389188:AAE1CVBTyLFkuKGrHX6-osUm1jRYu6CkTMw'
ADMIN_ID = 8048455578

bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')

@bot.message_handler(commands=['start'])
def send_start_message(message):
    welcome_text = (
        "<b>Welcome to the VIP DEXProxima Bot!</b>\n\n"
        "To gain <b>free lifetime access</b> to DEXProxima VIP:\n\n"
        "1 - Join ByBit using the button below\n"
        "2 - Deposit $100\n"
        "3 - Send your UID after this message!"
    )

    # ইনলাইন বাটন তৈরি
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Join ByBit", url="https://www.bybit.com/invite?ref=7MZ63O4"))

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

    # লোগো পাঠানো
    photo = open('/mnt/data/file-GfqkkdjKXKoT7gTvebMdMe', 'rb')
    bot.send_photo(message.chat.id, photo)

# UID (text) হ্যান্ডেল করে admin কে ফরোয়ার্ড এবং UID save করে
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_info = f"User: @{message.from_user.username or 'NoUsername'}\nUID: {message.text}\n"
    
    # এডমিনকে মেসেজ পাঠানো
    bot.send_message(ADMIN_ID, f"New UID received:\n{user_info}")
    
    # UID ফাইলে সংরক্ষণ
    with open("/mnt/data/uid_list.txt", "a") as f:
        f.write(user_info + "\n")
    
    # ইউজারকে রিপ্লাই
    bot.send_message(message.chat.id, "Thank you! Your UID has been received and is under review.")

# ছবি ফরোয়ার্ড
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Thank you! Your image has been received and is under review.")

bot.infinity_polling()