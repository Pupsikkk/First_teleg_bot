import time


def time_is_correct(some_time):
    some_time = some_time.strip(" ").split(":")
    return len(some_time) == 2 \
           and some_time[0].isdigit() and some_time[1].isdigit() \
           and -1 < int(some_time[0]) < 24 and -1 < int(some_time[1]) < 60


def date_is_correct(some_date):
    try:
        date = time.strptime(some_date, '%d.%m.%y')
        return True
    except ValueError:
        return False


def convert_to_correct_date(some_date):
    some_date = some_date.split(".")
    some_date[2] = "20" + some_date[2]
    some_date.reverse()
    return '-'.join(some_date)
