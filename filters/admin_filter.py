from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from database.core import DataBase
from database.requests.get import get_user_is_admin_by_tg_id



class IsAdmin(Filter):
    async def __call__(self, message: Message | CallbackQuery, db: DataBase) -> bool:

        if await get_user_is_admin_by_tg_id(db, message.from_user.id):
            return True
        else:
            if isinstance(message, CallbackQuery):
                await message.answer()
                await message.message.edit_text("❌ <b>Вы не администратор!</b>")
                return False
            else:
                await message.delete()
                await message.answer("❌ <b>Вы не администратор!</b>")
                return False
         