from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault

from database.requests import get_all_admins

user_commands = [
    BotCommand(command='start', description='♻️ Перезапустить бота'),
    BotCommand(command='support', description='☎️ Поддержка'),
    BotCommand(command='faq', description='❔ FAQ'),
]

admin_commands = [
    BotCommand(command='start', description='♻️ Перезапустить бота'),
    BotCommand(command='support', description='☎️ Поддержка'),
    BotCommand(command='faq', description='❔ FAQ'),
    BotCommand(command='db', description='📦 Получить Базу Данных'),
    BotCommand(command='log', description='🖨 Получить логи'),
]


async def set_commands(bot: Bot):
    await bot.set_my_commands(user_commands, scope=BotCommandScopeDefault())
    admins = list[int](await get_all_admins())
    for admin in admins:
        try:
            await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin))
        except:
            ...
