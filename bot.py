import telebot

import base_worker as bw
import group_parser as pr
import time_worker as tw

pr.__init__()
bw.__init__()

# Создаем экземпляр бота
bot = telebot.TeleBot('5240599342:AAHOmtjA9_fmctqHapE66UeFfqcycJNQLlw')

# Клавиатура бота
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row("🔙", "🔝", "🔜")

# Inline-клавиатура бота
inline_keyboard = telebot.types.InlineKeyboardMarkup(True)
inline_keyboard.add(telebot.types.InlineKeyboardButton(text="Четная", callback_data='even'))
inline_keyboard.add(telebot.types.InlineKeyboardButton(text="Нечетная", callback_data='odd'))


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


# Функция, обрабатывающая команду /time
@bot.message_handler(commands=["time"])
def check_base(m):
    bw.change_activity(m.chat.id, 0)
    bot.reply_to(m, tw.get_time())


# Функция, обрабатывающая команду /base
@bot.message_handler(commands=["week"])
def get_week(m):
    bw.change_activity(m.chat.id, 0)
    group_name = bw.get_group(m.chat.id)
    if group_name is not None:
        bot.send_message(m.chat.id, pr.print_week(group_name, tw.is_even_week_of_year()),
                         parse_mode='Markdown', reply_markup=inline_keyboard)
    else:
        bot.send_message(m.chat.id, "Вы не установили свою группу."
                                    "\nСделать это можно командой /set", parse_mode='Markdown')


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(m):
    activity = bw.get_activity(m.chat.id)
    if activity == 0:
        bot.send_message(m.chat.id, "Ожидаю вашей команды", reply_markup=None)
    elif activity == 1:
        if pr.is_group_exists(m.text):
            bw.change_group(m.chat.id, m.text.upper())
            bot.reply_to(m, "Группа установлена успешно!")
        else:
            bot.reply_to(m, "Такой группы не существует.")
        bw.change_activity(m.chat.id, 0)

    # bot.send_message(message.chat.id, 'Вы написали: ' + message.text, reply_markup=keyboard)
    # bot.send_message(message.chat.id, pr.print_week(message.text, 0), parse_mode='Markdown')


@bot.callback_query_handler(func=lambda call: True)
def callback_func(call):
    data = call.data
    if data == 'even':
        bot.edit_message_text(text=pr.print_week(bw.get_group(call.chat.id), 0)
                              , chat_id=call.chat.id, message_id=call.message.id)
    elif data == 'odd':
        bot.edit_message_text(text=pr.print_week(bw.get_group(call.chat.id), 1)
                              , chat_id=call.chat.id, message_id=call.message.id)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
