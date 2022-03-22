import telebot

import base_worker as bw
import group_parser as pr

pr.__init__()

# Создаем экземпляр бота
bot = telebot.TeleBot('5240599342:AAHOmtjA9_fmctqHapE66UeFfqcycJNQLlw')

# Клавиатура бота
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row("🔙", "🔝", "🔜")


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m):
    bot.send_message(m.chat.id,
                     'Добро пожаловать, я бот, показывающий расписание ИИТ\n/help - помощь',
                     reply_markup=keyboard)


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def start(m):
    bot.send_message(m.chat.id,
                     '/set - установить свою группу'
                     '\n/week - узнать расписание на эту неделю',
                     reply_markup=keyboard)


# Функция, обрабатывающая команду /set
@bot.message_handler(commands=["set"])
def start(m):
    if pr.is_group_exists(m.text):
        bw.change_group(m.chat.id, m.text)
        bot.reply_to(m, "Группа установлена успешно!")
    else:
        bot.reply_to(m, "Такой группы не существует.")


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    # bot.send_message(message.chat.id, 'Вы написали: ' + message.text, reply_markup=keyboard)
    bot.send_message(message.chat.id, pr.print_week(message.text, 0), parse_mode='Markdown')


# Запускаем бота
bot.polling(none_stop=True, interval=0)
