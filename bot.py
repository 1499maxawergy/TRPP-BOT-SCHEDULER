import telebot

# Создаем экземпляр бота
bot = telebot.TeleBot('5240599342:AAHOmtjA9_fmctqHapE66UeFfqcycJNQLlw')

# Клавиатура бота
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row("/previous", "/next")

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Я на связи. Напиши мне что-нибудь )', reply_markup=keyboard)


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text, reply_markup=keyboard)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
