import random

import telebot

import base_worker as bw
import group_parser as pr
import soup_worker
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
    bw.set_username(m.chat.id, m.from_user.username)
    bot.send_message(m.chat.id,
                     'Поздравляю с регистрацией, пользователь @'
                     + str(m.from_user.username)
                     + '!🤙\nЯ - бот, показывающий расписание ИИТ, ИИИ, ИРЭИ, ИТХТ в РТУ МИРЭА.'
                       '\n/help - команды для работы со мной.',
                     reply_markup=None)


# Функция, обрабатывающая команду /help
@bot.message_handler(commands=["help"])
def start_chatting(m):
    bw.set_username(m.chat.id, m.from_user.username)
    bot.send_message(m.chat.id,
                     '/set - установить свою группу.'
                     '\n/profile - узнать выбранную группу.'
                     '\n/week - узнать расписание на неделю.'
                     '\n/day - узнать расписание на день текущей недели.',
                     reply_markup=None)


# Функция, обрабатывающая команду /profile
@bot.message_handler(commands=["profile"])
def start_chatting(m):
    bw.set_username(m.chat.id, m.from_user.username)
    bot.send_message(m.chat.id,
                     'Привет, @' + str(m.from_user.username) + '!🖐\nВыбранная группа: ' + bw.get_group(m.chat.id),
                     reply_markup=None)


# Функция, обрабатывающая команду /set
@bot.message_handler(commands=["set"])
def set_group_to_user(m):
    bw.change_activity(m.chat.id, 1)
    bw.set_username(m.chat.id, m.from_user.username)
    bot.send_message(m.chat.id, "Введите свою группу в формате XXXX-XX-XX. Регистр букв не важен.", reply_markup=None)


# Функция, обрабатывающая команду /base
@bot.message_handler(commands=["base"])
def check_base(m):
    if m.chat.id == 680461201 or m.chat.id == 447163898:
        bw.change_activity(m.chat.id, 0)
        bot.send_message(m.chat.id, bw.get_base(), reply_markup=None)
    else:
        bw.set_username(m.chat.id, m.from_user.username)
        bot.send_message(m.chat.id, "Ожидаю вашей команды💤", reply_markup=None)


# Функция, обрабатывающая команду /msg
@bot.message_handler(commands=["msg"])
def send_msg(m):
    if m.chat.id == 680461201 or m.chat.id == 447163898:
        bw.change_activity(m.chat.id, 2)
        bot.send_message(m.chat.id, "Ожидаю текста для рассылки💤", reply_markup=None)
    else:
        bw.set_username(m.chat.id, m.from_user.username)
        bot.send_message(m.chat.id, "Ожидаю вашей команды💤", reply_markup=None)


# Функция, обрабатывающая команду /time
@bot.message_handler(commands=["time"])
def check_base(m):
    bw.change_activity(m.chat.id, 0)
    bw.set_username(m.chat.id, m.from_user.username)
    bot.reply_to(m, tw.get_time(), reply_markup=None)


# Функция, обрабатывающая команду /week
@bot.message_handler(commands=["week"])
def get_week(m):
    bw.change_activity(m.chat.id, 0)
    bw.set_username(m.chat.id, m.from_user.username)
    group_name = bw.get_group(m.chat.id)
    if group_name is not None:
        bot.send_message(m.chat.id, "Выберите неделю",
                         parse_mode='Markdown', reply_markup=inline_keyboard_week)
    else:
        bot.send_message(m.chat.id, "❗Вы не установили свою группу."
                                    "\nСделать это можно командой /set", parse_mode='Markdown', reply_markup=None)


# Функция, обрабатывающая команду /day
@bot.message_handler(commands=["day"])
def get_day(m):
    bw.change_activity(m.chat.id, 0)
    bw.set_username(m.chat.id, m.from_user.username)
    group_name = bw.get_group(m.chat.id)
    if group_name is not None:
        bot.send_message(m.chat.id, "Выберите день текущей недели",
                         parse_mode='Markdown', reply_markup=inline_keyboard_day)
    else:
        bot.send_message(m.chat.id, "❗Вы не установили свою группу."
                                    "\nСделать это можно командой /set", parse_mode='Markdown')


# Floppa
@bot.message_handler(commands=["floppa"])
def get_floppa(m):
    bw.set_username(m.chat.id, m.from_user.username)
    bot.send_message(m.chat.id, "Вы нашли секретную функцию! Испытайте свою удачу...🛀")
    random.seed()
    rand = random.randint(0, 10)
    if rand == 0:
        bot.send_photo(m.chat.id, "https://i.kym-cdn.com/photos/images/original/002/028/716/ef3.jpg", reply_markup=None)
        bot.send_message(m.chat.id, "Поздравляем, вам выпал Шлёппа в ванне!", reply_markup=None)
    else:
        bot.send_photo(m.chat.id, "https://memepedia.ru/wp-content/uploads/2020/10/big-floppa-meme.png",
                       reply_markup=None)
        bot.send_message(m.chat.id, "Вам выпал обычный Шлёппа. Попробуйте еще раз!", reply_markup=None)


# Получение сообщений от пользователя
@bot.message_handler(content_types=["text"])
def handle_text(m):
    activity = bw.get_activity(m.chat.id)
    bw.set_username(m.chat.id, m.from_user.username)
    if activity == 0:
        bot.send_message(m.chat.id, "Ожидаю вашей команды💤", reply_markup=None)
    elif activity == 1:
        if pr.is_group_exists(m.text):
            bw.change_group(m.chat.id, m.text.upper())
            bot.reply_to(m, "✅Группа установлена успешно!")
        else:
            bot.reply_to(m, "❗Такой группы не существует.")
        bw.change_activity(m.chat.id, 0)
    elif activity == 2:
        users = bw.get_users()
        for user in users:
            bot.send_message(int(str(user)[1:-2]), m.text, reply_markup=None)
        bw.change_activity(m.chat.id, 0)


# Обработка callback
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
        if tw.get_weekday() == 7:
            text = "Сегодня воскресенье! Выходной!🎉"
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
