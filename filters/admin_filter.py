from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from database.core import DataBase
from database.requests.get import get_user_is_admin



class IsAdmin(Filter):
    async def __call__(self, message: Message | CallbackQuery, db: DataBase) -> bool:

        if await get_user_is_admin(db, message.from_user.id):
            return True
        else:
            await message.answer("❌ <b>Вы не администратор!</b>")
            return False
         