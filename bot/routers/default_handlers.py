from aiogram import Router, Bot, F
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery

import database.requests as rq
import keyboards.admin_keyboards as ak
import keyboards.default_keyboards as dk
import keyboards.reply_keyboard as rk
import states.default_states as st
from utils.const_functions import get_support_text, get_hello_text

router = Router()
select_menu_item = 'Выберите пункт меню:'

@router.message(F.text.in_(('🔙 Главное меню', '/start')))
async def cmd_start(message: Message, bot: Bot, state: st.FSMContext) -> None:
    await state.clear()
    hello_text = get_hello_text()
    await rq.set_user(message.from_user.id, message.from_user.username)
    if (await rq.is_admin_user(message.from_user.id)):
        await message.answer(select_menu_item, reply_markup=rk.main_menu(message.from_user.id))
    else:
        await message.answer(hello_text, parse_mode='HTML')


@router.message(F.text == '❓ FAQ')
async def faq(message: Message, bot: Bot, state: st.FSMContext) -> None:
    await state.clear()
    await message.answer(f'{get_hello_text}')
    
@router.message(F.text == '🆘 Поддержка')
async def support(message: Message, bot: Bot, state: st.FSMContext) -> None:
    await state.clear()
    await message.answer(f'С какими вопросами вы хотите обратиться в поддержку?\n'+
                         f'\n{"```Советуем ввести USERNAME в телеграм для получения ответа по обращению```" if not message.from_user.username else None}')
    await state.set_state(st.Support_message.message_)
    
@router.message(st.Support_message.message_)
async def step1(message: Message, bot: Bot, state: st.FSMContext) -> None:
    await state.update_data(message_ = message.text)
    data = await state.get_data()
    admins = list[int](await rq.get_admins_id())
    support_text = get_support_text(username=message.from_user.username)
    if(message.from_user.username):
        for admin_id in admins:
            await bot.send_message(chat_id=admin_id, text=f'{support_text}{data["message_"]}')
    await state.clear()
    await rq.set_appeal(user_id=message.from_user.id, text=data["message_"], message_id=message.message_id) 
