from aiogram.fsm.state import State, StatesGroup


class AddTaskStates(StatesGroup):
    waiting_title = State()
    waiting_description = State()
    waiting_priority = State()


class BroadcastStates(StatesGroup):
    waiting_message = State()
    waiting_confirmation = State()
