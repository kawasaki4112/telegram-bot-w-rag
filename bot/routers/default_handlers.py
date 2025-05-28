from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from bot.states import states as st
from bot.utils.const_functions import get_hello_text
from bot.llm.llm import query_llm

router = Router()
select_menu_item = 'Выберите пункт меню:'

@router.message(F.text.in_(('🔙 Главное меню', '/start')))
async def start(message: Message, state: FSMContext):
    await message.answer(get_hello_text, parse_mode="HTML")
    await state.set_state(st.RequestState.waiting_for_request)

@router.message(st.RequestState.waiting_for_request)
async def process_name(message: Message, state: FSMContext):
    answer = await query_llm(message.text)
    await message.answer(answer, parse_mode="HTML")
    await state.clear()
