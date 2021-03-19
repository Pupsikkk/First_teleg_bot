import telebot
from sqlighter import *
from functions import *
import math
from telebot import types

TOKEN = "1755505537:AAGwgenPKX2utUWBf3ccurctG7SxzSer8DY"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_hand(message):
    with open('stikers/AnimatedSticker.tgs', 'rb') as stick:
        if message.chat.username == None:
            bot.send_message(message.chat.id, f" Придумай тег, дибіл")
        else:
            bot.send_message(message.chat.id, f"Приувет {message.chat.username}")
        bot.send_sticker(message.chat.id, stick)


# @bot.message_handler(commands=['dayTime'])
# def day_time_hand(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     item1 = types.KeyboardButton("Шпуньк1")
#     item2 = types.KeyboardButton("Шпуньк2")
#     markup.add(item1, item2)
#     bot.send_message(message.chat.id, "Кнопки", reply_markup=markup)

@bot.message_handler(commands=['addnote'])
def adding_note_command(message):
    add_some_status(message.from_user.id, "addnote")
    bot.send_message(message.chat.id,
                     "Введи время и то что делал к этому времени вот так:\n   21:21 - Флексил с бомжами")


@bot.message_handler(commands=['help'])
def help_command(message):
    bot.send_message(message.chat.id, "На данный момент основная роль бота это небольшой "
                                      "таймменеджмент. Вы можете добавлять на протяжении дня записи о своей "
                                      "деятельности и потом просмотреть как прошел ваш день и насколько полезным "
                                      "он был. \n\n Команды: \n /addnote -- добавление действия в список\n"
                                      "/viewday -- Увидеть проделанное сегодня\n"
                                      "/viewdaybydate -- Увидеть проделанное в какую то дату")


@bot.message_handler(commands=['viewday'])
def view_day_command(message):
    user_status = get_status(message.from_user.id)
    if user_status == 'none':
        inf = get_info_by_day(message.from_user.id, datetime.date.today())
        final_message = ''
        for i, line in enumerate(inf):
            if i != 0:
                final_message = final_message + f'От {inf[i - 1][0]} до {line[0]} -- {line[1]}\n\n '
            else:
                final_message = final_message + f'С момента пробуждения до {line[0]} -- {line[1]}\n\n '
        if final_message == '':
            bot.send_message(message.chat.id, "Ты ничего не записал, ленивая жопа")
        else:
            bot.send_message(message.chat.id, final_message)
    else:
        bot.send_message(message.chat.id, "Сначала заверши предыдущее действие (/exit)")


@bot.message_handler(commands=['viewdaybydate'])
def view_day_by_date_command(message):
    add_some_status(message.from_user.id, 'viewdaybydate')
    bot.send_message(message.chat.id, "Введи дату в таком формате:\n  29.04.02")


@bot.message_handler(commands=['exit'])
def exit_command(message):
    add_some_status(message.from_user.id, 'none')
    bot.send_message(message.chat.id, "Прервано")


@bot.message_handler(content_types=['text'])
def mes_hand(message):
    user_status = get_status(message.from_user.id)
    if user_status == 'addnote':
        text = message.text.split("-")
        if len(text) == 2 and time_is_correct(text[0]):
            time = text[0]
            if len(time.split(":")[0]) == 1:
                time = "0" + time.split(":")[0] + ":" + time.split(":")[1]
            add_note_to_db(message.from_user.id, message.chat.username, time, text[1])
            add_some_status(message.from_user.id, 'none')
            bot.send_message(message.chat.id, "Как скажешь! Я записал.")
        else:
            bot.send_message(message.chat.id, "Та ля, пиши как на примере показано:\n"
                                              "   19:00 — друзья позвали на вписку\n"
                                              "И не юзай больше одного знака '-'...")
    if user_status == 'viewdaybydate':
        if date_is_correct(message.text):
            inf = get_info_by_day(message.from_user.id, convert_to_correct_date(message.text))
            final_message = ''
            for i, line in enumerate(inf):
                if i != 0:
                    final_message = final_message + f'От {inf[i - 1][0]} до {line[0]} -- {line[1]}\n\n '
                else:
                    final_message = final_message + f'С момента пробуждения до {line[0]} -- {line[1]}\n\n '
            if final_message == '':
                bot.send_message(message.chat.id, "За этот день нет ни одной записи")
            else:
                bot.send_message(message.chat.id, final_message)
            add_some_status(message.from_user.id, 'none')
        else:
            bot.send_message(message.chat.id, "Дату вот так пишут:\n 28.10.01")
    if user_status == 'none':
        bot.send_message(message.chat.id, f"Хей, {message.chat.username} \n"
                                          f"Ты написал:\n"
                                          f"   {message.text}\n"
                                          f"Весело конечно, но я ничерта не понимаю))\n"
                                          f"Используй команды пж")


bot.polling(none_stop=True)
