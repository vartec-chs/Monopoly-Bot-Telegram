from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from database.core import DataBase
from database.requests.get import get_user_exists, get_user_is_blocked


class IsUserBlocked(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        
        db: DataBase = data.get("db")

        user_exists = await get_user_exists(db, event.from_user.id)
        user_is_blocked = await get_user_is_blocked(db, event.from_user.id)
        
        if not user_exists:
            return await handler(event, data)
        if not user_is_blocked:
            return await handler(event, data)
        else:
            await event.answer("❌ <b>Вы заблокированы в этом боте!</b>")


