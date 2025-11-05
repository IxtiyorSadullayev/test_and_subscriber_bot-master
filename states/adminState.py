from aiogram.fsm.state import State, StatesGroup

class AdminTanlov(StatesGroup):
    name = State()
    description = State()
    image = State()
    start_date = State()
    end_date = State()
    tekshiruv = State()


class TestCreate(StatesGroup):
    test_file = State()
    file_type = State()
    count_questions = State()
    answers = State()
    tekshiruv = State()

class Admin(StatesGroup):
    createTest = State()
    createTanlov = State()
    hisobot = State()