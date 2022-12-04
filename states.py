from aiogram.utils.helper import Helper, ListItem, HelperMode
class MyStates(Helper):
    mode = HelperMode.snake_case
    STATES_0 = ListItem()
    STATES_1 = ListItem()
    STATES_2 = ListItem()
    STATES_3 = ListItem()
    STATES_4 = ListItem()
    STATES_5 = ListItem()



class User:
    telegram_id = 0
    name = 'name'
    email = 'email'
    state = ''
    def __init__(self, telegram_id: int):
        self.state = MyStates.STATE_0
        self.telegram_id = telegram_id
    def __int__(self):
        return self.telegram_id
    def __str__(self):
        return f'{self.name} {self.email}'
    def __eq__(self, other):
        return other == self.telegram_id


if __name__ == '__main__':
    print(MyStates.all())
