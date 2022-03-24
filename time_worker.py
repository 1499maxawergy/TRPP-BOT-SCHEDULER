from datetime import datetime, timedelta


# get_weekday() - возврат дня недели (1 - понедельник, 2 - вторник ...)
def get_weekday():
    return (datetime.now() + timedelta(hours=3)).isocalendar()[2]


# is_even_week_of_year() - возврат 0 - неделя четная и 1 - неделя нечетная
def is_even_week_of_year():
    return (datetime.now() + timedelta(hours=3)).isocalendar()[1] % 2


# get_time() - возврат текущего времени
def get_time():
    return str((datetime.now() + timedelta(hours=3)).time())
