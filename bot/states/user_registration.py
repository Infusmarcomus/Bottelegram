from aiogram.fsm.state import State, StatesGroup

class RegistrationStates(StatesGroup):
    choosing_language = State()
    entering_name = State()