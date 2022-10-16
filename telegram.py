from aiogram import Bot, Dispatcher, executor, types
import os
import sqlite3

TOKEN = os.environ['token']
# print(TOKEN)
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# создание таблицы для хранения информации о пользователе
def create_users():
    connect = sqlite3.connect('users_data_base.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE users(
       id INT PRIMARY KEY,
       firstname TEXT,
       lastname TEXT,
       email TEXT,
       startLevel TEXT,
       payment TEXT);
    """)
    connect.commit()


# create_users()


# добавление новых позиций в БД из телеграмм бота
def add_users(users: dict):
    connect = sqlite3.connect('users_data_base.db')
    cursor = connect.cursor()
    request_in_users = f'INSERT INTO users' \
                       f' (id, firstname, lastname, email, startLevel, payment ) ' \
                       f'VALUES ' \
                       f'("{users["id"]}", "{users["firstname"]}","{users["lastname"]}","{users["email"]}","{users["startLevel"]}", "{users["payment"]}");'
    cursor.execute(request_in_users)
    connect.commit()

# функция для удаления строк
# def delete_record():
#     sqlite_connection = sqlite3.connect('users_data_base.db')
#     cursor = sqlite_connection.cursor()
#
#     sql_delete_query = """DELETE from users where id = 0"""
#     cursor.execute(sql_delete_query)
#     sqlite_connection.commit()
#     cursor.close()
#
# delete_record()

users1={}
# получение информации от пользователя из телеграмма
@dp.message_handler()
async def echo(message: types.Message):
    print(message)
    print(message.from_user.id, ' - ', message.from_user.first_name, ' - ', message.text)
    # создание словаря с хранением данных о пользователе и дополнительные поля,
    # которые заполнятся позже (пока значения по умолчанию)
    users1.update({'id':message.from_user.id,
                'firstname':message.from_user.first_name,
                'lastname':message.from_user.last_name,
                'email': 'fjfj@jj',
                'startLevel':'beg',
                'payment':'tr'
    })
    add_users(users1)
    text = f'Пользователь {message.from_user.first_name} написал {message.text}'
    print(text)


if __name__ == '__main__':
    executor.start_polling(dp)