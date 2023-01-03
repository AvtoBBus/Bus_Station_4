import telebot
import config
import os.path
import time
import csv
import get_schedule as gs

from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def welcome(message):
    list_info = []
    with open("data/info.txt", encoding='utf-8') as file:
        list_info = file.readlines()

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("/change")
    markup.add(item1)

    sti = open('data/stickers/HI.webp', 'rb')
    bot.send_sticker(message.chat.id, sti)

    bot.send_message(
        message.chat.id, "Приветик, {0.first_name}!\nЯ бот Эдди, призванный помогать в учёбе\n".format(message.from_user))

    bot.send_message(
        message.chat.id, list_info)

    received_message_text = bot.send_message(
        message.chat.id, "Нажми \"/change\" чтобы начать", reply_markup=markup)

    bot.register_next_step_handler(received_message_text, change_option)


@bot.message_handler(commands=['change'])
def change_option(message):
    write_in_file = True
    with open("users.csv", "r", encoding="utf-8") as file:
        readerder = csv.reader(file, delimiter=";")
        for row in readerder:
            if row[1] == str(message.from_user.id):
                write_in_file = False
    if write_in_file:
        with open("users.csv", "a", newline="", encoding="utf-8") as file:
            printer = csv.writer(file, delimiter=";")
            printer.writerow([
                message.from_user.first_name,
                message.from_user.id
            ])

    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Узнать задание по лабе")
    item2 = types.KeyboardButton("Достать учебник")
    item3 = types.KeyboardButton("Получить секретик")
    item4 = types.KeyboardButton("Узнать расписание")
    item5 = types.KeyboardButton("Важные ссылки")

    markup.add(item1, item2, item3, item4, item5)

    received_message_text = bot.send_message(
        message.chat.id, "Погнали!", reply_markup=markup)
    bot.register_next_step_handler(received_message_text, expanded_change)


@bot.message_handler(content_types=['text'])
def expanded_change(message):
    if message.chat.type == 'private':
        if message.text == 'Узнать задание по лабе':
            sti1 = open('data/stickers/REALLY.webp', 'rb')
            bot.send_sticker(message.chat.id, sti1)
            markup = types.ReplyKeyboardRemove()
            list_items = []
            list_files = os.listdir("data/labs_book/labs/")
            list_files.sort()
            for files in list_files:
                list_items.append(files)
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True)
            for item in list_items:
                markup.add(item)
            item = types.KeyboardButton("Вернуться в меню")
            markup.add(item)
            received_message_text = bot.send_message(
                message.chat.id, "Что именно нужно?", reply_markup=markup)
            bot.register_next_step_handler(
                received_message_text, change_lab_task)

        elif message.text == 'Достать учебник':
            sti2 = open('data/stickers/YES.webp', 'rb')
            bot.send_sticker(message.chat.id, sti2)
            markup = types.ReplyKeyboardRemove()
            bot.send_message(message.chat.id, 'Окей', reply_markup=markup)

            list_items = []
            list_files = os.listdir("data/labs_book/")
            list_files.sort()
            for files in list_files:
                list_items.append(files)
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, one_time_keyboard=True)
            for item in list_items:
                if str(item) != "labs":
                    markup.add(item)
            item = types.KeyboardButton("Вернуться в меню")
            markup.add(item)

            received_message_text = bot.send_message(
                message.chat.id, "По какому предмету?", reply_markup=markup)
            bot.register_next_step_handler(received_message_text, change_book)

        elif message.text == 'Получить секретик':
            file = open("allowed_users.csv", "r", encoding="utf-8")
            readerder = csv.reader(file, delimiter=";")
            locked = True
            for row in readerder:
                if str(row[0]) == str(message.from_user.id):
                    locked = False
            if locked == False:
                received_message = bot.send_message(
                    message.chat.id, "Ура! У тебя есть доступ!\nНапиши, что угодно. чтобы продолжить!")
                bot.register_next_step_handler(received_message, change_secret)
            else:
                markup = types.ReplyKeyboardMarkup(
                    resize_keyboard=True, one_time_keyboard=True)
                item1 = types.KeyboardButton("/change")
                markup.add(item1)
                received_message = bot.send_message(
                    message.chat.id, "Блинб, у тебя нет доступа(\nНажми \"/change\" чтобы продолжить", reply_markup=markup)
                bot.register_next_step_handler(received_message, change_option)

        elif message.text == 'Узнать расписание':
            sti1 = open('data/stickers/REALLY.webp', 'rb')
            bot.send_sticker(message.chat.id, sti1)
            markup = types.ReplyKeyboardRemove()
            received_message = bot.send_message(
                message.chat.id, "Введи мне номер своей группы, номер недели который тебе нужен и номер дня недели\n\n!!! Format: 6101-010302D 17 5 !!!", reply_markup=markup)
            bot.register_next_step_handler(received_message, send_shedule)

        elif message.text == 'Важные ссылки':
            important_links(message)

        elif message.text == 'Вернуться в меню':
            change_option(message)

        else:
            error(message)


def error(message):
    sti3 = open('data/stickers/IDK.webp', 'rb')
    bot.send_sticker(message.chat.id, sti3)
    markup = types.ReplyKeyboardRemove()
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("/start")
    markup.add(item1)
    received_message_text = bot.send_message(
        message.chat.id, 'Блинб, я не знаю, что ответить(((\nНажми \"/start\" чтобы продолжить', reply_markup=markup)
    bot.register_next_step_handler(received_message_text, welcome)


def open_file(way_to_file):
    return os.path.exists(way_to_file)


def important_links(message):
    markup = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "ИИК Приём - https://vk.com/iik.ssau.priem\nСтуд. совет ИИК - https://vk.com/sciic\nРасписание ИИК - https://ssau.ru/rasp/faculty/492430598?course=1\nSSAU - https://ssau.ru\n", reply_markup=markup)
    change_option(message)


def send_shedule(message):
    if not os.path.isdir('AllGroupShedule'):
        gs.pars_all_group()
    try:
        num_group = message.text.split()[0]
        selectedWeek = message.text.split()[1]
        selectedWeekday = message.text.split()[2]
        url_schedule = gs.find_schedule_url(
            num_group, selectedWeek, selectedWeekday)
        shedule = gs.pars_shedule(url_schedule)
        bot.send_message(
            message.chat.id, shedule + f"\nURL: {url_schedule}")
        change_option(message)
    except:
        error(message)


def change_lab_task(message):
    list_items = []
    list_files = []
    if message.text == 'ООП':
        list_files = os.listdir("data/labs_book/labs/ООП")
        for files in list_files:
            list_items.append(files)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for item in list_items:
            markup.add(item)
        item = types.KeyboardButton("Вернуться в меню")
        markup.add(item)
        received_message = bot.send_message(
            message.chat.id, "Номер?", reply_markup=markup)
        bot.register_next_step_handler(received_message, send_pdf)
    elif message.text == 'ОНИ':
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)

        list_files = os.listdir("data/labs_book/labs/ОНИ")
        for files in list_files:
            list_items.append(files)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for item in list_items:
            markup.add(item)
        item = types.KeyboardButton("Вернуться в меню")
        markup.add(item)

        received_message = bot.send_message(
            message.chat.id, "Номер?", reply_markup=markup)
        bot.register_next_step_handler(received_message, send_pdf)
    elif message.text == 'ОП':
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)

        list_files = os.listdir("data/labs_book/labs/ОП")
        for files in list_files:
            list_items.append(files)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for item in list_items:
            markup.add(item)
        item = types.KeyboardButton("Вернуться в меню")
        markup.add(item)

        received_message = bot.send_message(
            message.chat.id, "Номер?", reply_markup=markup)
        bot.register_next_step_handler(received_message, send_pdf)
    elif message.text == 'Вернуться в меню':
        change_option(message)
    else:
        error(message)


def change_book(message):
    list_items = []
    list_files = []
    markup = types.ReplyKeyboardRemove()
    if message.text == 'Алгебра_и_Геометрия':
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)

        list_files = os.listdir("data/labs_book/Алгебра_и_Геометрия")
        for files in list_files:
            list_items.append(files)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for item in list_items:
            markup.add(item)
        item = types.KeyboardButton("Вернуться в меню")
        markup.add(item)
        received_message = bot.send_message(
            message.chat.id, "Автор?", reply_markup=markup)
        bot.register_next_step_handler(received_message, send_pdf)
    elif message.text == 'Мат_Анализ':
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)

        list_files = os.listdir("data/labs_book/Мат_Анализ")
        for files in list_files:
            list_items.append(files)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for item in list_items:
            markup.add(item)
        item = types.KeyboardButton("Вернуться в меню")
        markup.add(item)

        received_message = bot.send_message(
            message.chat.id, "Автор?", reply_markup=markup)
        bot.register_next_step_handler(received_message, send_pdf)
    elif message.text == 'Теор_Вероят_и_СП':
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)

        list_files = os.listdir("data/labs_book/Теор_Вероят_и_СП")
        for files in list_files:
            list_items.append(files)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for item in list_items:
            markup.add(item)
        item = types.KeyboardButton("Вернуться в меню")
        markup.add(item)

        received_message = bot.send_message(
            message.chat.id, "Что именно?", reply_markup=markup)
        bot.register_next_step_handler(received_message, send_pdf)
    elif message.text == 'Английский':
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)

        list_files = os.listdir("data/labs_book/Английский")
        for files in list_files:
            list_items.append(files)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for item in list_items:
            markup.add(item)
        item = types.KeyboardButton("Вернуться в меню")
        markup.add(item)

        received_message = bot.send_message(
            message.chat.id, "Что именно?", reply_markup=markup)
        bot.register_next_step_handler(received_message, send_pdf)
    elif message.text == 'Мат_Логика_Теор_Алгоритмов':
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)

        list_files = os.listdir("data/labs_book/Мат_Логика_Теор_Алгоритмов")
        for files in list_files:
            list_items.append(files)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for item in list_items:
            markup.add(item)
        item = types.KeyboardButton("Вернуться в меню")
        markup.add(item)

        received_message = bot.send_message(
            message.chat.id, "Автор?", reply_markup=markup)
        bot.register_next_step_handler(received_message, send_pdf)
    elif message.text == 'Физика':
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)

        list_files = os.listdir("data/labs_book/Физика")
        for files in list_files:
            list_items.append(files)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for item in list_items:
            markup.add(item)
        item = types.KeyboardButton("Вернуться в меню")
        markup.add(item)

        received_message = bot.send_message(
            message.chat.id, "Автор?", reply_markup=markup)
        bot.register_next_step_handler(received_message, send_pdf)
    elif message.text == 'История':
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)

        list_files = os.listdir("data/labs_book/История")
        for files in list_files:
            list_items.append(files)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        for item in list_items:
            markup.add(item)
        item = types.KeyboardButton("Вернуться в меню")
        markup.add(item)

        received_message = bot.send_message(
            message.chat.id, "Автор?", reply_markup=markup)
        bot.register_next_step_handler(received_message, send_pdf)
    elif message.text == 'Вернуться в меню':
        change_option(message)
    else:
        error(message)


def change_secret(message):
    list_items = []
    for doc in os.listdir("secret"):
        list_items.append(doc)
    markup = types.ReplyKeyboardMarkup(
        resize_keyboard=True, one_time_keyboard=True)
    for item in list_items:
        markup.add(item)
    item = types.KeyboardButton("Вернуться в меню")
    markup.add(item)
    received_message = bot.send_message(
        message.chat.id, "Какой секретик нужен?", reply_markup=markup)
    bot.register_next_step_handler(received_message, send_secret)


def send_secret(message):
    if not message.text == 'Вернуться в меню':
        bot.send_message(message.chat.id, "Отправляю!")
        file = open(f"secret/{message.text}", "rb")
        bot.send_document(message.chat.id, file)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton("/change")
        markup.add(item1)
        received_message = bot.send_message(
            message.chat.id, "Нажми \"/change\" чтобы продолжить", reply_markup=markup)
        bot.register_next_step_handler(received_message, change_option)
    else:
        change_option(message)


def send_pdf(message):
    if message.text == 'Вернуться в меню':
        change_option(message)
    else:
        way_to_file = ""
        start_search = True
        while start_search:
            for subject in os.listdir("data/labs_book/"):
                way_to_file = f"data/labs_book/{subject}/{message.text}"
                if open_file(way_to_file):
                    start_search = False
                    break
            if start_search:
                while start_search:
                    for subject in os.listdir("data/labs_book/labs/"):
                        way_to_file = f"data/labs_book/labs/{subject}/{message.text}"
                        if open_file(way_to_file):
                            start_search = False
                            break
        needed_book = open(way_to_file, 'rb')
        bot.send_message(message.chat.id, "Отправляю")
        bot.send_document(message.chat.id, needed_book)
        sti = open('data/stickers/NYA.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        markup = types.ReplyKeyboardMarkup(
            resize_keyboard=True, one_time_keyboard=True)
        item1 = types.KeyboardButton("/change")
        markup.add(item1)
        received_message = bot.send_message(
            message.chat.id, "Нажми \"/change\" чтобы продолжить", reply_markup=markup)
        bot.register_next_step_handler(received_message, change_option)


# RUN
while True:
    try:
        bot.polling(none_stop=True)
    except:
        time.sleep(15)
