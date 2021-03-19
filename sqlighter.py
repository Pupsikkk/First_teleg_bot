import sqlite3
import datetime

def add_some_status(user_id, status):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query = f"""SELECT * FROM status_reg WHERE user_id = {user_id}"""
        cursor.execute(query)
        buf = list(cursor)
        if len(buf) == 1:
            query = f"""UPDATE status_reg SET status = '{status}' WHERE user_id = '{user_id}' """
            cursor.execute(query)
        else:
            query = f"""INSERT INTO status_reg (user_id, status) VALUES ('{user_id}', '{status}')"""
            cursor.execute(query)

def get_status(user_id):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        query = f"""SELECT * FROM status_reg WHERE user_id = {user_id}"""
        cursor.execute(query)
        buf = list(cursor)
        if len(buf) == 0:
            add_some_status(user_id, "none")
            return 'none'
        else:
            return buf[0][1]

def add_note_to_db(user_id, username, time, message):
    with sqlite3.connect('database.db') as db:
        cursor = db.cursor()
        add_time = str(datetime.datetime.now()).split(" ")[1].split(".")[0][:-3]
        query = f""" INSERT INTO register_by_date (user_id, username,Date, datetime, what_i_do, addTime) VALUES (
            '{user_id}',
            '{username}',
            '{datetime.date.today()}',
            '{time}',
            '{message}',
            '{add_time}'
            )"""
        cursor.execute(query)

def get_info_by_day(user_id, date):
    with sqlite3.connect('database.db')as db:
        cursor = db.cursor()
        query = f"""SELECT datetime, what_i_do FROM register_by_date WHERE user_id = '{user_id}' AND Date = '{date}' ORDER BY datetime"""
        cursor.execute(query)
        return list(cursor)
