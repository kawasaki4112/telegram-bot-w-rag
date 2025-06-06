from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.states import states as st
from bot.utils.const_functions import get_hello_text
from bot.llm.llm import query_llm
from bot.utils.misc.bot_logging import bot_logger

router = Router()

@router.message(F.text.in_(('🔙 Главное меню', '/start')))
async def start(message: Message, state: FSMContext):
    await state.clear()
    text = get_hello_text()
    await message.answer(text, parse_mode="HTML")
    await state.set_state(st.RequestState.waiting_for_request)

@router.message(st.RequestState.waiting_for_request)
async def process_request(message: Message, state: FSMContext):
    try:
        answer = await query_llm(message.text, message.from_user.id)
        # answer = "answer"
    except Exception as e:
        bot_logger.exception("Ошибка при запросе к LLM: ", e)
        await message.answer(
            "Произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте позже."
        )
        return
    if not answer:
        await message.answer(
            "К сожалению, я не смог найти ответ на ваш вопрос. Попробуйте переформулировать его."
        )
        await state.set_state(st.RequestState.waiting_for_request)
    else:
        await message.answer(answer, parse_mode="HTML")
