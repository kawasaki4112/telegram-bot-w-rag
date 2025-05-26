from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import database.requests as rq

async def main_menu(user_id: int) -> ReplyKeyboardMarkup:
    user = await rq.get_user(user_id)
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(KeyboardButton('❓ FAQ'), KeyboardButton('🆘 Поддержка'))
    if user.is_admin:
        keyboard.row(KeyboardButton('⚙️ Настройки'), KeyboardButton('🔍 Поиск'), KeyboardButton('👨‍💼 Админ панель'))

    return keyboard.as_markup()

async def settings_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        KeyboardButton("🖍 Изменить данные"), KeyboardButton("🕹 Выключатели"),
    ).row(
        KeyboardButton("🔙 Главное меню"),
    )

    return keyboard.as_markup()

async def admin_frep() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    keyboard.row(
        KeyboardButton("Список админов"), KeyboardButton("Список обращений")
    ).row(KeyboardButton("🕹 Добавить админа"), KeyboardButton("Удалить админа")
    ).row(KeyboardButton("🔙 Главное меню")
    )

    return keyboard.as_markup()