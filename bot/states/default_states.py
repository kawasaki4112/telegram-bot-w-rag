from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

class Support_message(StatesGroup):
    message_: str