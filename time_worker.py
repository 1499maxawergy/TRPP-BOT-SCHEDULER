"""Работа с временем на сервере через модуль datetime"""
from datetime import datetime, timedelta


# get_weekday() - возврат дня недели (1 - понедельник, 2 - вторник ...)
def get_weekday():
    """Возвращает текущий день недели

    Возвращает текущий день недели для GMT+3 на момент запроса
    (1 - ПН, ..., 7 - ВС)"""
    return (datetime.now() + timedelta(hours=3)).isocalendar()[2]


# is_even_week_of_year() - возврат 0 - неделя четная и 1 - неделя нечетная
def is_even_week_of_year():
    """Возвращает четность недели

    Возвращает четность неделя для GMT+3 на момент запроса
    (0 - четная, 1 - нечетная)"""
    return (datetime.now() + timedelta(hours=3)).isocalendar()[1] % 2


# get_time() - возврат текущего времени
def get_time():
    """Возврашает текущее время (MSK)

    Так как вуз находится в Москве, то функция вернет время
     GMT+3"""
    return str((datetime.now() + timedelta(hours=3)).time())
