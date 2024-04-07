from aiogram.fsm.state import StatesGroup, State


class SignUpStatesGroup(StatesGroup):
    """
    Набор состояний пользователя при регистрации
    и записи на занятие
    """
    GET_NAME = State()
    GET_PHONE_NUMBER = State()

    SELECT_DIRECTION = State()
    SELECT_SESSION = State()
