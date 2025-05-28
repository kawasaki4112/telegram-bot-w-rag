# - *- coding: utf- 8 - *-
from aiogram import BaseMiddleware
from aiogram.types import User

from bot.database.requests import user_crud as rq


# Проверка юзера в БД и его добавление
class ExistsUserMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        this_user: User = data.get("event_from_user")

        if not this_user.is_bot:
            get_user = await rq.get(tg_id = this_user.id)

            user_id = this_user.id
            user_login = this_user.username

            if user_login is None: user_login = ""

            if get_user is None:
                await rq.create(tg_id = user_id, username = user_login.lower())
            else:
                if user_login.lower() != get_user.user_login:
                    await rq.update(filters={"tg_id": get_user.user_id}, updates={"username": user_login.lower()})

        return await handler(event, data)
