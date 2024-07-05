from aiogram.filters.state import StatesGroup, State


class SG(StatesGroup):
    MAIN = State()
    SKILLS = State()
    JOB_TITLE = State()
    FULL_NAME = State()
    CHOOSE = State()
    EMPLOYMENT = State()
