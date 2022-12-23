import sqlite3

class DataBase:
    def __init__(self, db_name: str='bot.users'):
        self.__db_name = f'{db_name}.sqlite'
        self.__conn = sqlite3.connect(self.__db_name)

    def setup(self, table: str, data: dict):
        keys = list(data.keys())
        values = list(data.values())
        req = f'CREATE TABLE IF NOT EXISTS "{table}"('
        for i in range(len(keys)):
            req += f'"{keys[i]}" {values[i]}, '
        req = req[:-2] + ')'
        self.__conn.cursor()
        self.__conn.execute(req)
        self.__conn.commit()

    def add_item(self, table: str, data: dict):
        columns = ''
        values = ''
        for i in range(len(data.keys())):
            columns += f'"{list(data.keys())[i]}", '
            values += f'"{list(data.values())[i]}", '
        columns = columns[:-2]
        values = values[:-2]

        req = f'INSERT INTO "{table}"' \
              f' ({columns}) ' \
              f'VALUES ' \
              f'({values});'
        # print(req)
        self.__conn.cursor()
        self.__conn.execute(req)
        self.__conn.commit()

    def get_item(self, table: str, data: dict):
        curs = self.__conn.cursor()
        req = f'SELECT {list(data.keys())[0]} FROM "{table}"'
        select = curs.execute(req, )
        select_data = select.fetchone()
        self.__conn.commit()
        if select_data is None:
            return data

    def add_user(self, data: dict):
        get = f'INSERT INTO Users (' \
              f'telegram_id, ' \
              f'first_name, ' \
              f'last_name, ' \
              f'phone, ' \
              f'email' \
              f') VALUES (' \
              f'"{data["telegram_id"]}", ' \
              f'"{data["first_name"]}", ' \
              f'"{data["first_name"]}", ' \
              f'"{data.get("phone")}", ' \
              f'"{str(data.get("email"))}", ' \
              f');'
        self.__conn.cursor()
        self.__conn.execute(get)
        self.__conn.commit()
        self.__conn.commit()

    def get_user(self, telegram_id: int):
        curs = self.__conn.cursor()
        get = f'SELECT * FROM Users WHERE telegram_id="{telegram_id}"'
        result = curs.execute(get)
        data = result.fetchall()
        print(data)
        return data

    def update_user(self, telegram_id: int, data: dict):
        key = list(data.keys())[0]
        value = list(data.values())[0]
        req = f'UPDATE Users SET {key} = "{value}" WHERE telegram_id="{telegram_id}"'
        self.__conn.cursor()
        self.__conn.execute(req)
        self.__conn.commit()

    def delete_user(self, table: str, item_text):
        pass

    def delete_table(self, table: str):
        req = f'DROP TABLE IF EXISTS "{table}"'
        self.__conn.cursor()
        self.__conn.execute(req)
        self.__conn.commit()
        self.__conn.close()


DataBase()
db = DataBase()
db.setup(table='Users',
               data={
                    'telegram_id': 'integer primary key',
                    'first_name': 'string',
                    'last_name': 'string',
                    'phone': 'string',
                    'email': 'string',
                })


