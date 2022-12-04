from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import bd, random

bd = bd.DataBase()

menu = ['Add Personal Info', 'Translator', 'Video Lessons','Gramma in Picture','Show Personal Info']
keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard_menu.add(KeyboardButton('MAIN'))
for i in menu:
    keyboard_menu.insert(i)
# keyboard_menu.add(KeyboardButton('Show Personal Info'))


def get_kbrd():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    # for user in get_users():
    #     menu.insert(KeyboardButton(user[3]))
    menu.row(
        KeyboardButton('Phone', request_contact=True),
        KeyboardButton('Email',))
    menu.add(KeyboardButton('MAIN'))
    return menu

def more_kbrd():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu.row(KeyboardButton('More', ))
    menu.add(KeyboardButton('MAIN'))
    return menu

def get_kbrd_translate():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu.add(KeyboardButton('Завершить перевод'))
    return menu


# def inline_keyboard():
#     btn1 = InlineKeyboardButton(text='Video lessons', callback_data= 'https://en.islcollective.com/video-lessons/search')
#     btn2 = InlineKeyboardButton(text='Check yourself', callback_data= 'How to translate?')
#     btn3 = InlineKeyboardButton(text='English in picture', callback_data='button3')
#     kbrd = InlineKeyboardMarkup(resize_keyboard=True, row_width=2).add(btn1, btn2, btn3)
#     return kbrd