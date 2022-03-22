import telebot

import base_worker as bw
import group_parser as pr

pr.__init__()
bw.__init__()

# Создаем экземпляр бота
bot = telebot.TeleBot('5240599342:AAHOmtjA9_fmctqHapE66UeFfqcycJNQLlw')

# Клавиатура бота
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row("🔙", "🔝", "🔜")


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m):
    bw.change_activity(m.chat.id, 0)
    bot.send_message(m.chat.id,
                     'Поздравляю с регистрацией, пользователь '
                     + str(m.chat.id)
                     + '.\nЯ бот, показывающий расписание ИИТ В РТУ МИРЭА'
                       '\n/help - команды для работы со мной',
                     reply_markup=None)


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def start_chatting(m):
    bot.send_message(m.chat.id,
                     '/set - установить свою группу'
                     '\n/week - узнать расписание на эту неделю',
                     reply_markup=None)


# Функция, обрабатывающая команду /set
@bot.message_handler(commands=["set"])
def set_group_to_user(m):
    bw.change_activity(m.chat.id, 1)
    bot.reply_to(m, "Введите свою группу в формате XXXX-XX-XX. Регистр букв не важен.")


# Функция, обрабатывающая команду /base
@bot.message_handler(commands=["base"])
def check_base(m):
    bw.change_activity(m.chat.id, 0)
    bot.reply_to(m, bw.get_base())


# Функция, обрабатывающая команду /base
@bot.message_handler(commands=["week"])
def get_week(m):
    bw.change_activity(m.chat.id, 0)
    group_name = bw.get_group(m.chat.id)
    bot.send_message(m.chat.id, pr.print_week(group_name, 0), parse_mode='Markdown')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(m):
    activity = bw.get_activity(m.chat.id)
    if activity == 0:
        bot.send_message(m.chat.id, "Ожидаю вашей команды", reply_markup=None)
    elif activity == 1:
        if pr.is_group_exists(m.text):
            bw.change_group(m.chat.id, m.text)
            bot.reply_to(m, "Группа установлена успешно!")
        else:
            bot.reply_to(m, "Такой группы не существует.")
        bw.change_activity(m.chat.id, 0)

    # bot.send_message(message.chat.id, 'Вы написали: ' + message.text, reply_markup=keyboard)
    # bot.send_message(message.chat.id, pr.print_week(message.text, 0), parse_mode='Markdown')


# Запускаем бота
bot.polling(none_stop=True, interval=0)
