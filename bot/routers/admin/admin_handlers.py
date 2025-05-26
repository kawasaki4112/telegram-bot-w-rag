import re

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

import database.requests as rq
import keyboards.admin_keyboards as ak
import states.admin_states as st

router = Router()
select_menu_item = 'Выберите пункт меню:'

@router.callback_query(F.data == 'admins')
async def admins(callback: CallbackQuery):
    # Обработка нажатия на кнопку "admins"
    await callback.message.edit_text(text = select_menu_item, reply_markup = ak.admins_menu)

@router.callback_query(F.data == 'back_to_admins_menu')
async def back_to_admins_menu(callback: CallbackQuery):
    # Обработка нажатия на кнопку "back_to_admins_menu"
    await callback.message.edit_text(text=select_menu_item, reply_markup=ak.admins_menu)

@router.callback_query(F.data == 'show_all_admins')
async def show_all_admins(callback: CallbackQuery):
    # Обработка нажатия на кнопку "show_all_admins"
    all_admins_text = 'Все админы:\n'
    all_admins = await rq.get_all_admins()
    for admin in all_admins:
        all_admins_text+=f'@{admin.user_id if not admin.username else admin.username}\n'
    await callback.message.edit_text(text = all_admins_text)
    await callback.message.answer(text=select_menu_item, reply_markup=ak.admins_menu)

@router.callback_query(F.data == 'add_admin')
async def add_admin(callback: CallbackQuery, state: st.FSMContext):
    # Обработка нажатия на кнопку "add_admin"
    await state.clear()
    await state.set_state(st.Add_admin.user)
    await callback.message.edit_text("Введите USERNAME или выберите из списка", reply_markup=await ak.users())

@router.callback_query(F.data.startswith('add_users_page_'))
async def form(callback: CallbackQuery):
    # Обработка нажатия на кнопку "add_users_page_"
    page = int(callback.data.split('_')[-1])
    markup = await ak.users(page)
    await callback.message.edit_reply_markup(reply_markup=markup)

@router.callback_query(F.data.startswith('add_admin_'))
async def form(callback: CallbackQuery, state: st.FSMContext):
    # Обработка нажатия на кнопку "add_admin_"
    user_id = int(callback.data.split('_')[-1])
    user = await rq.get_user(user_id)
    await state.update_data(user = user.user_id)

    is_added = await rq.add_admin_in_bd(user_id=user.user_id)
    await callback.message.answer(f'{is_added}')
    await callback.message.answer(text=select_menu_item, reply_markup=ak.admins_menu)
    await state.clear()

@router.message(st.Add_admin.user)
async def step1(message: Message, state: st.FSMContext):
    # Обработка ввода USERNAME для добавления админа
    await state.update_data(user = message.text)
    user = await rq.get_user(message.text)
    
    if not user:
        await message.answer("Пользователь не найден!")
        await message.answer(text=select_menu_item, reply_markup=ak.admins_menu)
        await state.clear()
    else:
        is_added = await rq.add_admin_in_bd(user_id=user.user_id)
        await message.answer(f'{is_added}')
        await message.answer(text=select_menu_item, reply_markup=ak.admins_menu)
        await state.clear()

@router.callback_query(F.data == 'delete_admin')
async def delete_admin(callback: CallbackQuery, state: st.FSMContext):
    # Обработка нажатия на кнопку "delete_admin"
    await state.clear()
    await state.set_state(st.Delete_admin.user)
    await callback.message.edit_text("Введите USERNAME или выберите из списка", reply_markup=await ak.admins())

@router.callback_query(F.data.startswith('delete_admins_page_'))
async def form(callback: CallbackQuery):
    # Обработка нажатия на кнопку "delete_admins_page_"
    page = int(callback.data.split('_')[-1])
    markup = await ak.admins(page)
    await callback.message.edit_reply_markup(reply_markup=markup)
    
@router.callback_query(F.data.startswith('delete_admin_'))
async def form(callback: CallbackQuery, state: st.FSMContext):
    # Обработка нажатия на кнопку "delete_admin_"
    await state.clear()
    id = int(callback.data.split('_')[-1])
    await callback.message.answer(text=await rq.delete_admin_from_bd(id))
    await callback.message.answer(select_menu_item, reply_markup=ak.admins_menu)

@router.message(st.Delete_admin.user)
async def step1(message: Message, state: st.FSMContext):
    # Обработка ввода USERNAME для удаления админа
    await state.update_data(user = message.text)
    data = await state.get_data()
    user = await rq.get_user(data["user"])
    
    await message.answer(f'{str(await rq.delete_admin_from_bd(user.user_id))}')
    await message.answer(text=select_menu_item, reply_markup=ak.admins_menu)
    await state.clear()

@router.callback_query(F.data == 'back_to_admin_menu')
async def back_to_admin_menu(callback: CallbackQuery):
    # Обработка нажатия на кнопку "back_to_admin_menu"
    await callback.message.edit_text(text=select_menu_item, reply_markup=ak.ad_main_menu)

@router.callback_query(F.data == 'settings_menu')
async def settings(callback: CallbackQuery):
    # Обработка нажатия на кнопку "settings"
    await callback.message.edit_text(text=select_menu_item, reply_markup=await ak.settings_menu())
    
@router.callback_query(F.data.startswith('setting_'))
async def form(callback: CallbackQuery):
    # Обработка нажатия на кнопку "setting_"
    state = str(callback.data.split('_')[-1])
    await callback.message.answer(text=select_menu_item, reply_markup=await ak.setting())
