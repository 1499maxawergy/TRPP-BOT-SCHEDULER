from datetime import datetime


# get_weekday вернет день недели, пример: понедельник-1, вторник-2, ..., воскресенье-7
def get_weekday():
    return datetime.now().isocalendar()[2]


# is_even_week_of_year вернет 0 - если неделя четная и 1 - если неделя нечетная
def is_even_week_of_year():
    return datetime.now().isocalendar()[1] % 2
