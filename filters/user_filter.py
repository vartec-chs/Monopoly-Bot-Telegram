from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from database.core import DataBase
from database.requests.get import get_user_exists


class IsUserExists(Filter):

    async def __call__(self, ctx: Message | CallbackQuery, db: DataBase) -> bool:
        
        tg_id = ctx.from_user.id

        return await get_user_exists(db, tg_id)

        

