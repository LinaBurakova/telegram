import os
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from states import MyStates, User
import bd
import keyboards as kb
import translators as ts
import re
import emoji

bd = bd.DataBase()
TOKEN = '5677022662:AAGhuoMRImgWYu1mX01OP4_Vh8SgeKxMHOs'
print(TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

users = {}
# состояние, при котором бот отправляет фото из папки img уроков по грамматике
# в соответствии с выбранной темой из содержания
@dp.message_handler(state=MyStates.STATES_0)
async def word_test(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    chat_id = message.from_user.id
    numb = list(range(1, 49))
    for i in numb:
        if message.text == f'{i}':
            keyboard=kb.get_menu()
            await bot.send_photo(chat_id=message.from_user.id, photo=types.InputFile(f'img/{i}.jpg'))
            await message.answer(f'{emoji.emojize("✅")}Для перехода в главное меню нажмите - /main. '
                                 '\nTo go to the main menu enter  - /main', reply_markup=keyboard)
    commands = ['MAIN MENU', '/main', 'Word Translator', '/translate', 'Add Personal Info', '/contacts', 'Video Lessons',
                '/videolessons', 'Gramma in Picture', '/grammainpicture', 'Show Personal Info', '/showpersonalinfo',
                '/cancel']
    for i in commands:
        if message.text == i:
            keyboard = kb.keyboard_menu
            await message.answer(f'{emoji.emojize("✅")}Выберите новое действие из "Главного меню" / Choose a new command from "MAIN MENU', reply_markup=keyboard)
            await state.set_state('*')
            if message.text == 'Word Translator':
                await state.set_state(MyStates.all()[2])
            elif message.text == 'Add Personal Info':
                await state.set_state(MyStates.all()[3])
# проверка ввода сообщения на необходимые значения (от 1 до 48), исходя из количества тем.
# если введенное сообщение не принадлежит списку commands, то отправляем
# сообщение "Try again" и заставляем пользователя вводить правильное значение
# если введенное сообщение принадлежит списку commands, то перебрасываем в соответствующее состояние
    if message.text.isalpha():
        await message.answer(f'{emoji.emojize("😞")}Попробуй снова / Try again')
    elif message.text.isdigit():
        if int(message.text)>=49:
            await message.answer(f'{emoji.emojize("😞")}Попробуй снова / Try again')
# состояние, при котором бот запрашивает пользователя ввести телефон
# эту информацию заносим в нашу базу данных
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
# состояние, при котором бот выполняет перевод слов благодаря установленному модулю translators
# изначально делаем проверку на русский/английский алфавит? чтобы определить с какого языка будем переводить
# переводчик останавливается только при принудительном завершении (нажатие на команду или кнопкой клавиатуры)
@dp.message_handler(state=MyStates.STATES_2)
async def name(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    chat_id = message.from_user.id
    if message.text == '/cancel' or message.text == 'end' or message.text == 'Stop translator':
        keyboard = kb.keyboard_menu
        await message.answer('The end',reply_markup=keyboard)
        await state.set_state('*')
    else:
        if bool(re.search('[а-яА-Я]', message.text)) == False:
            translate = ts.google(message.text, to_language='ru')
            keyboard = kb.get_kbrd_translate()
            await message.answer(f'Перевод с английского / Translation from English {emoji.emojize("🔤")}')
            await bot.send_message(chat_id=message.from_user.id, text=translate)
        else:
            translate = ts.google(message.text, to_language='en')
            keyboard = kb.get_kbrd_translate()
            await message.answer(f'Перевод с русского / Translation from Russian {emoji.emojize("🔤")}')
            await bot.send_message(chat_id=message.from_user.id, text=translate)
        await message.answer(f"Для остановки переводчика введите - /cancel {emoji.emojize('❌')}\n To stop the translator, enter - /cancel {emoji.emojize('❌')}",reply_markup=keyboard)
# состояние, при котором бот запрашивает пользователя ввести электронную почту
# после чего переносимся в следующее состояние, где проверяем корректность ввода email
@dp.message_handler(state=MyStates.STATES_3)
async def user_data(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == 'MAIN MENU' or message.text == '/main':
        keyboard = kb.keyboard_menu
        await message.answer(message.text, reply_markup=keyboard)
        await state.set_state('*')
    elif message.text == 'Email':
        text = f'Введите свой email / Enter your email {emoji.emojize("💌")}'
        await bot.send_message(chat_id=message.from_user.id, text=text)

        await state.set_state(MyStates.all()[4])
# с помощью регулярного выражения проверяем валидность email
# при неправильном вводе просим вводить заново
# при правильном - возврат в главное меню и добавлению электронного адреса в БД
@dp.message_handler(state=MyStates.STATES_4)
async def user_data(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    chat_id = message.from_user.id
    pattern = r"^[a-zA-Z0-9]{1,100}[@][a-z]{2,6}\.[a-z]{2,4}"
    number_re = re.compile(pattern)
    if message.text == 'MAIN MENU' or message.text == '/main':
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
# проверка на существование пользователя в БД
# если такого нет, то заносим информацию в базу
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
# если пользователь на начальном этапе что-то написал в чат,
# то ему присылают ответное сообщение что необходимо делать дальше
    if message.text.isalnum():
        keyboard = kb.keyboard_menu
        await message.answer(f'Нажми /start для начала работы {emoji.emojize("✅")}/ Enter /start to start work {emoji.emojize("✅")}', reply_markup=keyboard)
    elif message.text == 'Start' or message.text == '/start' or message.text == 'start' or message.text == '/main':
        keyboard = kb.keyboard_menu
        await message.answer(f"Hello {message.from_user.first_name} {message.from_user.last_name}! Select an action from the'MAIN MENU' to get started ☺", reply_markup=keyboard)
    elif message.text == '/help' or message.text == 'help' or message.text == 'Help':
        await message.answer(f"Этот бот поможет тебе изучить английский {emoji.emojize('🇬🇧')}или станет твоим личным переводчиком.Просто нажми 'Let's begin'{emoji.emojize('💪')} и после этого выбери нужную категорию.\n\nThis bot will help you learn English {emoji.emojize('🇬🇧')} or become your personal translator.Just click on 'Let's begin'{emoji.emojize('💪')} and then select the category you want.")
# отправляет пользователю ссылки на обучающие видео с помощью инлайн кнопок
    elif message.text == 'Video Lessons' or message.text == '/videolessons':
        keyboard = kb.more_kbrd()
        await message.answer(f'Видео материалы для тебя / Video materials for you {emoji.emojize("🎥")}: ', reply_markup = keyboard)
# отправляет пользователю меню с нумерацией тем, после чего переносит в состояние,
# где отправляет соответствующее фото урока по заданному номеру
    elif message.text == 'Gramma in Picture' or message.text == '/grammainpicture':
        state = dp.current_state(user=chat_id)
        keyboard = kb.get_menu()
        await bot.send_photo(chat_id=message.from_user.id, photo=types.InputFile('img/0.jpg'))
        await message.answer(f'Введите число необходимой темы / Enter the number of topics {emoji.emojize("🔢")}', reply_markup = keyboard)
        await state.set_state(MyStates.all()[0])
# отправляет пользователю запрос на получения от него данных
    elif message.text == 'Add Personal Info' or message.text == '/contacts':
        state = dp.current_state(user=chat_id)
        keyboard = kb.get_kbrd()
        await state.set_state(MyStates.all()[3])
        await message.answer(f"Введите свой email и телефон для подписки на наши обновления.{emoji.emojize('📱')} \nEnter your email and share your contact to subscribe for our updates.{emoji.emojize('📱')}",reply_markup=keyboard)
# запрашивает у пользователя фразу для перевода, затем переходит в состояние,
# где проверяет язык введенного сообщения и выполняет перевод
    elif message.text == '/translate' or message.text == 'Word Translator':
        state = dp.current_state(user=chat_id)
        await message.answer(f"Введите слово или фразу для перевода / Enter a word or phrase to translate {emoji.emojize('🇬🇧')}")
        await state.set_state(MyStates.all()[2])
# показывает пользователю информацию, которую хранит бот у себя в БД
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
