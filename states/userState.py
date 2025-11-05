from aiogram.fsm.state import State, StatesGroup

class User(StatesGroup):
    tg_id = State()
    user_name = State()
    user_phone = State()
    user_role = State()
    tekshiruv = State()

class TestAnswersFromUser(StatesGroup):
    test_code = State()
    answers = State()
    tekshiruv = State()

class UserActions(StatesGroup):
    work_test = State()
    tanlovlar = State()
    about_bot = State()