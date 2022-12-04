import os
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from states import MyStates, User
import bd
import keyboards
import keyboards as kb
import random
import translators as ts
import re
import emoji
from validate_email import validate_email

bd = bd.DataBase()

TOKEN = '5677022662:AAEDlga6kam3c-T6lCCOHcSDKGwhqScx404'
print(TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

users = {}

@dp.message_handler(commands='start')
async def start(m, res=False):
    await bot.send_message(m.chat.id, f"Hello {m.from_user.first_name} {m.from_user.last_name}! Enter 'MAIN' to get started ☺")

@dp.message_handler(commands="help")
async def help(m, res=False):
    await bot.send_message(m.chat.id, f"Этот бот поможет тебе изучить английский {emoji.emojize('🇬🇧')}или станет твоим личным переводчиком.Просто нажми 'Let's begin'{emoji.emojize('💪')} и после этого выбери нужную категорию.\n\nThis bot will help you learn English {emoji.emojize('🇬🇧')} or become your personal translator.Just click on 'Let's begin'{emoji.emojize('💪')} and then select the category you want.")

@dp.message_handler(state=MyStates.STATES_0)
async def word_test(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    chat_id = message.from_user.id
    numb = list(range(1, 49))
    for i in numb:
        if message.text == f'{i}':
            await bot.send_photo(chat_id=message.from_user.id, photo=types.InputFile(f'img/{i}.jpg'))
            await message.answer(f'{emoji.emojize("✅")}Для перехода в главное меню нажмите - /main '
                                 '\nTo go to the main menu enter  - /main')
    commands = ['MAIN', 'main', 'Translator', '/translate', 'Add Personal Info', '/contacts', 'Video Lessons',
                '/videolessons', 'Gramma in Picture', '/grammainpicture', 'Show Personal Info', '/showpersonalinfo',
                '/cancel']
    for i in commands:
        if message.text == i:
            keyboard = kb.keyboard_menu
            await message.answer(f'{emoji.emojize("✅")}Выберите новое действие из "Главного меню" / Choose a new command from "MAIN"', reply_markup=keyboard)
            await state.set_state('*')
    if message.text.isalpha():
        await message.answer(f'{emoji.emojize("😞")}Попробуй снова / Try again')
    elif message.text.isdigit():
        if int(message.text)>=49:
            await message.answer(f'{emoji.emojize("😞")}Попробуй снова / Try again')


@dp.message_handler(content_types='contact', state=MyStates.STATES_3)
async def ph(message: types.Message):
    chat_id = message.from_user.id
    state = dp.current_state(user=chat_id)
    print(message.contact.phone_number)
    print(message.from_id)
    phone = {
        'phone': message.contact.phone_number,
    }
    bd.update_user(telegram_id=message.from_id, data=phone)
    # await state.set_state(MyStates.all()[2])
    await bot.send_message(chat_id=message.from_user.id, text= f"Спасибо за Ваш контакт / Thank's for your contact {emoji.emojize('💗')}")


@dp.message_handler(state=MyStates.STATES_2)
async def name(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    chat_id = message.from_user.id

    if message.text == '/cancel' or message.text == 'end':
        await message.answer('The end')
        await state.set_state('*')
    else:
        if bool(re.search('[а-яА-Я]', message.text)) == False:
            translate = ts.google(message.text, to_language='ru')
            await message.answer(f'Перевод с английского / Translation from English {emoji.emojize("🔤")}')
            await bot.send_message(chat_id=message.from_user.id, text=translate)

        else:
            translate = ts.google(message.text, to_language='en')
            await message.answer(f'Перевод с русского / Translation from Russian {emoji.emojize("🔤")}')
            await bot.send_message(chat_id=message.from_user.id, text=translate)

        await message.answer(f"Для остановки переводчика введите - /cancel {emoji.emojize('❌')}\n To stop the translator, enter - /cancel {emoji.emojize('❌')}")

@dp.message_handler(state=MyStates.STATES_3)
async def user_data(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == 'MAIN' or message.text == '/main':
        keyboard = kb.keyboard_menu
        await message.answer(message.text, reply_markup=keyboard)
        await state.set_state('*')
    elif message.text == 'Email':
        text = f'Введите свой email / Enter your email {emoji.emojize("💌")}'
        await bot.send_message(chat_id=message.from_user.id, text=text)

        await state.set_state(MyStates.all()[4])


@dp.message_handler(state=MyStates.STATES_4)
async def user_data(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    chat_id = message.from_user.id
    pattern = r"^[a-zA-Z0-9]{1,100}[@][a-z]{2,6}\.[a-z]{2,4}"
    number_re = re.compile(pattern)
    if message.text == 'MAIN' or message.text == '/main':
        keyboard = kb.keyboard_menu
        await message.answer(message.text, reply_markup=keyboard)
        await state.set_state('*')
    else:
        # if number_re.findall(message.text):
        if bool(re.search(pattern, message.text)) == True:
            await message.answer(f"Спасибо за Вашу электронную почту / Thank's for your email {emoji.emojize('💗')}")
            keyboard = kb.keyboard_menu
            await message.answer(message.text, reply_markup=keyboard)
            await state.set_state('*')
        else:
            await message.answer(f"Попробуйте еще раз, введите электронную почту следующего формата: example@gmail.com {emoji.emojize('📩')} / Try again, enter email format like: example@gmail.com {emoji.emojize('📩')}")
        email = {
                'email': message.text,
            }
        bd.update_user(telegram_id=message.from_id, data=email)
        # await state.set_state(MyStates.all()[3])


@dp.message_handler(state=MyStates.STATES_5)
async def video_less(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == 'MAIN' or message.text == '/main':
        keyboard = kb.keyboard_menu
        await message.answer(message.text, reply_markup=keyboard)
        await state.set_state('*')
    elif message.text == 'More':
        keyboard = kb.more_kbrd()
        await message.answer(message.text, reply_markup=keyboard)
        await message.answer('http://klassikaknigi.info/video-uroki-anglijskogo-yazyka/')
        await message.answer('https://en.islcollective.com/english-esl-video-lessons')
        await message.answer(f'{emoji.emojize("✅")}Чтобы вернуться в главное меню, нажмите - "MAIN" / Enter "MAIN" to return to the main menu',reply_markup=keyboard)
        await state.set_state('*')


@dp.message_handler(state='*')
async def echo(message: types.Message):
    chat_id = message.from_user.id
    user = {
                'telegram_id': f'{message.from_user.id}',
                'first_name': f'{message.from_user.first_name}',
                'last_name': f'{message.from_user.last_name}',}

    users.update({message.from_user.id: {message.from_user.first_name: message.from_user.last_name}})

    if len(bd.get_user(message.from_user.id)) == 0:
        bd.add_item(table='Users', data=user)
    users.update({message.from_user.id: message.from_user.first_name})
    state = dp.current_state(user=chat_id)
    await state.set_state(MyStates.all()[1])

    if message.text == '/start' or message.text == 'Start' or message.text == 'MAIN' or message.text == '/main' or message.text.isalpha():
        keyboard = kb.keyboard_menu
        await message.answer(message.text, reply_markup=keyboard)

    elif message.text == 'Video Lessons' or message.text == '/videolessons':
        await message.answer(f'Видео материалы для тебя / Video materials for you {emoji.emojize("🎥")}: ')
        await message.answer('https://vse-kursy.com/onlain/language/english/free/')
        keyboard = kb.more_kbrd()
        await message.answer(message.text, reply_markup = keyboard)
        await state.set_state(MyStates.all()[5])


    elif message.text == 'Gramma in Picture' or message.text == '/grammainpicture':
        state = dp.current_state(user=chat_id)
        await bot.send_photo(chat_id=message.from_user.id, photo=types.InputFile('img/0.jpg'))
        await message.answer(f'Введите число необходимой темы / Enter the number of topics {emoji.emojize("🔢")}')
        await state.set_state(MyStates.all()[0])

    elif message.text == 'Add Personal Info' or message.text == '/contacts':
        state = dp.current_state(user=chat_id)
        keyboard = kb.get_kbrd()
        await state.set_state(MyStates.all()[3])
        await message.answer(f"Введите свой email и телефон для подписки на наши обновления.{emoji.emojize('📱')} \nEnter your email and share your contact to subscribe for our updates.{emoji.emojize('📱')}",reply_markup=keyboard)

    elif message.text == '/translate' or message.text == 'Translator':
        state = dp.current_state(user=chat_id)
        await message.answer(f"Введите слово или фразу для перевода / Enter a word or phrase to translate {emoji.emojize('🇬🇧')}")
        await state.set_state(MyStates.all()[2])

    elif message.text == 'Show Personal Info' or message.text == '/showpersonalinfo':
        user = bd.get_user(message.from_user.id)
        user_text = f'Personal Info {emoji.emojize("😎")}:\n' \
                    f'telegram_id: {user[0][0]}\n' \
                    f'first_name: {user[0][1]}\n' \
                    f'last_name: {user[0][2]}\n' \
                    f'phone: {user[0][3]}\n' \
                    f'email: {user[0][4]}\n'
        await message.answer(user_text)


@dp.callback_query_handler()
async def call_echo(callback_q: types.CallbackQuery):
    await bot.answer_callback_query(callback_q.id)
    await bot.send_message(chat_id=callback_q.from_user.id, text=callback_q.data)

if __name__ == '__main__':
    executor.start_polling(dp)
