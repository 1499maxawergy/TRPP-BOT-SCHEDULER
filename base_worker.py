import os

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import group_parser


DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


# init() - создает базу данных
def __init__():
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users ("
                   "id serial NOT NULL PRIMARY KEY,"
                   "chat_id bigint UNIQUE NOT NULL,"
                   "group_name VARCHAR(16),"
                   "activity integer"
                   ");")
    cursor.close()


# change_group() - изменение группу пользователя
def change_group(chat_id, group_name):
    if group_parser.is_group_exists(group_name):
        cursor = con.cursor()
        cursor.execute("INSERT INTO users(chat_id, group_name) VALUES(%s, %s)"
                       "ON CONFLICT(chat_id) DO UPDATE SET group_name = %s",
                       (chat_id, group_name, group_name))
        cursor.close()


# get_group() - получение группу пользователя
def get_group(chat_id):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE chat_id = %s" % chat_id)
    row = cursor.fetchone()
    cursor.close()

    if row is not None:
        return row[2]
    return None


# change_activity() - изменение статуса пользователя
def change_activity(chat_id, value):
    cursor = con.cursor()
    cursor.execute("INSERT INTO users(chat_id, activity) VALUES(%s, %s)"
                   "ON CONFLICT(chat_id) DO UPDATE SET activity = %s",
                   (chat_id, value, value))
    cursor.close()


# get_activity() - получение статуса пользователя
def get_activity(chat_id):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE chat_id = %s" % chat_id)
    row = cursor.fetchone()
    cursor.close()

    if row is not None:
        return row[3]
    return None


# get_base() - получение полной базы данных
def get_base():
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    cursor.close()

    out_line = ""
    if rows is not None:
        for row in rows:
            out_line += ' '.join(str(x) for x in row) + '\n'
    return out_line


# get_users() - получение списка пользователей
def get_users():
    cursor = con.cursor()
    cursor.execute("SELECT chat_id FROM users")
    rows = cursor.fetchall()
    cursor.close()
    return rows
