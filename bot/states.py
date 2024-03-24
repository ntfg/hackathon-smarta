from aiogram.dispatcher.filters.state import State, StatesGroup

class WordStates(StatesGroup):
    word = State()