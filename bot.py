import telebot

import base_worker as bw
import group_parser as pr
import time_worker as tw

pr.__init__()
bw.__init__()

# Создаем экземпляр бота
bot = telebot.TeleBot('5240599342:AAHOmtjA9_fmctqHapE66UeFfqcycJNQLlw')

# Inline-week-клавиатура бота
inline_keyboard_week = telebot.types.InlineKeyboardMarkup()
inline_keyboard_week.add(telebot.types.InlineKeyboardButton(text="Текущая", callback_data='current'))
inline_keyboard_week.add(telebot.types.InlineKeyboardButton(text="Четная", callback_data='even'))
inline_keyboard_week.add(telebot.types.InlineKeyboardButton(text="Нечетная", callback_data='odd'))

# Inline-day-клавиатура бота
inline_keyboard_day = telebot.types.InlineKeyboardMarkup()
inline_keyboard_day.add(telebot.types.InlineKeyboardButton(text="Сегодня", callback_data='current_day'))
inline_keyboard_day.add(telebot.types.InlineKeyboardButton(text="ПН", callback_data='day-1'),
                        telebot.types.InlineKeyboardButton(text="ВТ", callback_data='day-2'),
                        telebot.types.InlineKeyboardButton(text="СР", callback_data='day-3'))
inline_keyboard_day.add(telebot.types.InlineKeyboardButton(text="ЧТ", callback_data='day-4'),
                        telebot.types.InlineKeyboardButton(text="ПТ", callback_data='day-5'),
                        telebot.types.InlineKeyboardButton(text="СБ", callback_data='day-6'))


# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m):
    bw.change_activity(m.chat.id, 0)
    bot.send_message(m.chat.id,
                     'Поздравляю с регистрацией, пользователь @'
                     + str(m.from_user.username)
                     + '.\nЯ бот, показывающий расписание ИИТ В РТУ МИРЭА'
                       '\n/help - команды для работы со мной',
                     reply_markup=None)


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def start_chatting(m):
    bot.send_message(m.chat.id,
                     '/set - установить свою группу'
                     '\n/profile - узнать выбранную группу'
                     '\n/week - узнать расписание на неделю'
                     '\n/day - узнать расписание на день текущей недели',
                     reply_markup=None)


# Функция, обрабатывающая команду /profile
@bot.message_handler(commands=["profile"])
def start_chatting(m):
    bot.send_message(m.chat.id,
                     'Привет, @' + str(m.from_user.username) + '\nВыбранная группа - ' + bw.get_group(m.chat.id),
                     reply_markup=None)


# Функция, обрабатывающая команду /set
@bot.message_handler(commands=["set"])
def set_group_to_user(m):
    bw.change_activity(m.chat.id, 1)
    bot.send_message(m.chat.id, "Введите свою группу в формате XXXX-XX-XX. Регистр букв не важен.", reply_markup=None)


# Функция, обрабатывающая команду /base
@bot.message_handler(commands=["base"])
def check_base(m):
    if m.chat.id == 680461201 or m.chat.id == 447163898:
        bw.change_activity(m.chat.id, 0)
        bot.send_message(m.chat.id, bw.get_base(), reply_markup=None)
    else:
        bot.send_message(m.chat.id, "Ожидаю вашей команды", reply_markup=None)


@bot.message_handler(commands=["msg"])
def send_msg(m):
    if m.chat.id == 680461201 or m.chat.id == 447163898:
        bw.change_activity(m.chat.id, 0)
        users = bw.get_users()
        for user in users:
            # bot.send_message(user, bw.get_base(), parse_mode='Markdown', reply_markup=None)
            print(int(str(user)[1:-2]))
    else:
        bot.send_message(m.chat.id, "Ожидаю вашей команды", reply_markup=None)


# Функция, обрабатывающая команду /time
@bot.message_handler(commands=["time"])
def check_base(m):
    bw.change_activity(m.chat.id, 0)
    bot.reply_to(m, tw.get_time(), reply_markup=None)


# Функция, обрабатывающая команду /week
@bot.message_handler(commands=["week"])
def get_week(m):
    bw.change_activity(m.chat.id, 0)
    group_name = bw.get_group(m.chat.id)
    if group_name is not None:
        bot.send_message(m.chat.id, "Выберите неделю",
                         parse_mode='Markdown', reply_markup=inline_keyboard_week)
    else:
        bot.send_message(m.chat.id, "Вы не установили свою группу."
                                    "\nСделать это можно командой /set", parse_mode='Markdown', reply_markup=None)


# Функция, обрабатывающая команду /day
@bot.message_handler(commands=["day"])
def get_day(m):
    bw.change_activity(m.chat.id, 0)
    group_name = bw.get_group(m.chat.id)
    if group_name is not None:
        bot.send_message(m.chat.id, "Выберите день текущей недели",
                         parse_mode='Markdown', reply_markup=inline_keyboard_day)
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
def callback_handler(call):
    data = call.data
    if data == 'current':
        bot.edit_message_text(text=pr.print_week(bw.get_group(call.message.chat.id),
                                                 tw.is_even_week_of_year())
                              , chat_id=call.message.chat.id, message_id=call.message.id,
                              parse_mode='Markdown')
    elif data == 'even':
        bot.edit_message_text(text=pr.print_week(bw.get_group(call.message.chat.id), 1)
                              , chat_id=call.message.chat.id, message_id=call.message.id,
                              parse_mode='Markdown')
    elif data == 'odd':
        bot.edit_message_text(text=pr.print_week(bw.get_group(call.message.chat.id), 0)
                              , chat_id=call.message.chat.id, message_id=call.message.id,
                              parse_mode='Markdown')
    elif data == 'current_day':
        text = ""
        if tw.get_weekday() == 7:
            text = "Сегодня воскресенье! Выходной!"
        else:
            text = pr.print_day(bw.get_group(call.message.chat.id), tw.is_even_week_of_year(), tw.get_weekday())
        bot.edit_message_text(text=text, chat_id=call.message.chat.id, message_id=call.message.id,
                              parse_mode='Markdown')
    elif data.startswith("day"):
        day = int(data.split("-")[1])
        bot.edit_message_text(text=pr.print_day(bw.get_group(call.message.chat.id), tw.is_even_week_of_year(), day),
                              chat_id=call.message.chat.id, message_id=call.message.id,
                              parse_mode='Markdown')


# Запускаем бота
bot.polling(none_stop=True, interval=0)
