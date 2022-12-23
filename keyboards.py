from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import bd
bd = bd.DataBase()

menu = ['Add Personal Info', 'Word Translator', 'Video Lessons','Gramma in Picture','Show Personal Info']
keyboard_menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
keyboard_menu.add(KeyboardButton('MAIN MENU'))
for i in menu:
    keyboard_menu.insert(i)

def get_kbrd():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu.row(
        KeyboardButton('Phone', request_contact=True),
        KeyboardButton('Email',))
    menu.add(KeyboardButton('MAIN MENU'))
    return menu

def more_kbrd():
    btn = InlineKeyboardButton(text='Видео уроки английского языка', url='http://klassikaknigi.info/video-uroki-anglijskogo-yazyka/')
    btn1 = InlineKeyboardButton(text='Islcollective', url='https://en.islcollective.com/english-esl-video-lessons')
    btn2 = InlineKeyboardButton(text='Islcollective', url='https://vse-kursy.com/onlain/language/english/free/')
    kbrd = InlineKeyboardMarkup().add(btn,btn1,btn2)
    return kbrd

def get_kbrd_translate():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu.add(KeyboardButton('Stop translator'))
    return menu
def get_menu():
    menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    menu.add(KeyboardButton('MAIN MENU'))
    return menu