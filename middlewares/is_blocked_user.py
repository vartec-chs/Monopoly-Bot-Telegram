from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from database.core import DataBase
from database.requests.get import get_user_exists, get_user_is_blocked_by_tg_id


class IsUserBlocked(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:
        
        db: DataBase = data.get("db")

        user_exists = await get_user_exists(db, event.from_user.id)
        user_is_blocked = await get_user_is_blocked_by_tg_id(db, event.from_user.id)
        
        if not user_exists:
            return await handler(event, data)
        if not user_is_blocked:
            return await handler(event, data)
        else:
            if isinstance(event, CallbackQuery):
                await event.message.answer("❌ <b>Вы заблокированы в этом боте!</b>")
            else:
                await event.answer("❌ <b>Вы заблокированы в этом боте!</b>")


