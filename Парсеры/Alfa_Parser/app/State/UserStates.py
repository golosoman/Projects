from aiogram.dispatcher.filters.state import State, StatesGroup


class UserStates(StatesGroup):
    """
    Группа состояний для пользователя.

    Атрибуты:
        code: Состояние, представляющее ввод кода пользователем.
    """
    code = State()
    click_rate = State()
    user_answer = State()
