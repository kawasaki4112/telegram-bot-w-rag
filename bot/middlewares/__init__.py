from aiogram import Dispatcher

from bot.middlewares.middleware_throttling import ThrottlingMiddleware
from bot.middlewares.middleware_user import ExistsUserMiddleware

def register_all_middlwares(dp: Dispatcher):
    dp.callback_query.outer_middleware(ExistsUserMiddleware())
    dp.message.outer_middleware(ExistsUserMiddleware())

    dp.message.middleware(ThrottlingMiddleware())
