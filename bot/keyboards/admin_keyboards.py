from aiogram.types import (InlineKeyboardMarkup, 
                           InlineKeyboardButton)

from aiogram.utils.keyboard import InlineKeyboardBuilder

import database.requests as rq

per_page = 10


admins_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text = 'Все admin', callback_data='show_all_admins')],
    [InlineKeyboardButton(text = 'Добавить admin', callback_data='add_admin')],
    [InlineKeyboardButton(text = 'Удалить admin', callback_data='delete_admin')],
    [InlineKeyboardButton(text = 'Назад', callback_data='back_to_admin_menu')]
])



#########################################################################################
######################################## Функции ########################################
#########################################################################################

async def settings_data():
    settings = await rq.get_settings()
    keyboard = InlineKeyboardBuilder()
    for setting in settings:
        keyboard.row(InlineKeyboardButton(text = f'{setting.text} - {setting.value if setting.value else setting.bool_value}',
                                          callback_data = f'setting_{setting.name}'))
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='back_to_admin_menu'))
    return keyboard.as_markup()

async def settings_tumblers():
    settings = await rq.get_settings()
    keyboard = InlineKeyboardBuilder()
    for setting in settings:
        keyboard.row(InlineKeyboardButton(text = f'{setting.text} - {setting.value if setting.value else setting.bool_value}',
                                          callback_data = f'setting_{setting.name}'))
    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='back_to_admin_menu'))
    return keyboard.as_markup()

async def users(page: int = 1):
    all_users_result = await rq.get_all_users()
    all_users = list(all_users_result)

    start_idx = (page - 1) * per_page 
    end_idx = start_idx + per_page 
    paginated_users = all_users[start_idx:end_idx]
    
    keyboard = InlineKeyboardBuilder()

    for user in paginated_users:
        if not user.is_admin:
            keyboard.row(InlineKeyboardButton(
                text=user.username if user.username else str(user.user_id),
                callback_data=f'add_admin_{user.user_id}'
            ))

    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text='Prev', callback_data=f'add_users_page_{page - 1}'))
    if end_idx < len(all_users):
        nav_buttons.append(InlineKeyboardButton(text='Next', callback_data=f'add_users_page_{page + 1}'))
    
    if nav_buttons:
        keyboard.row(*nav_buttons)  # Добавляем Prev и Next в один ряд

    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='back_to_admins_menu'))

    return keyboard.as_markup()

async def admins(page: int = 1):
    all_users_result = await rq.get_all_admins()
    all_users = list(all_users_result)

    start_idx = (page - 1) * per_page 
    end_idx = start_idx + per_page 
    paginated_users = all_users[start_idx:end_idx]
    
    keyboard = InlineKeyboardBuilder()

    for user in paginated_users:
        keyboard.row(InlineKeyboardButton(
            text=user.username if user.username else str(user.user_id),
            callback_data=f'delete_admin_{user.user_id}'
        ))

    nav_buttons = []
    if page > 1:
        nav_buttons.append(InlineKeyboardButton(text='Prev', callback_data=f'delete_admins_page_{page - 1}'))
    if end_idx < len(all_users):
        nav_buttons.append(InlineKeyboardButton(text='Next', callback_data=f'delete_admins_page_{page + 1}'))
    
    if nav_buttons:
        keyboard.row(*nav_buttons)  # Добавляем Prev и Next в один ряд

    keyboard.row(InlineKeyboardButton(text='Назад', callback_data='back_to_admins_menu'))

    return keyboard.as_markup()
