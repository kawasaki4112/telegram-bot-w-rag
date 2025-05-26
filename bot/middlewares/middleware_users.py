from aiogram import BaseMiddleware
from aiogram.types import User

from bot.database.requests import get_user, set_user
from bot.utils.const_functions import clear_html


class ExistsUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        this_user: User = data.get("event_from_user")

        if not this_user.is_bot:
            await set_user(user_id=this_user.id, username=this_user.username)

        return await handler(event, data)
