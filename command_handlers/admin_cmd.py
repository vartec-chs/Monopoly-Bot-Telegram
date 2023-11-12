from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database.core import DataBase
from database.requests.get import get_count_games, get_count_users

from filters.admin_filter import IsAdmin

from keyboards.admin_kb import admin_menu


router = Router(name=__name__)



@router.message(Command("admin"), IsAdmin())
async def admin(message: Message, db: DataBase):
    await message.delete()

    # tg_id = message.from_user.id

    content = f"🛡️ <b>Админ меню:</b>\n\n"\
    f"👥 <u>Всего пользователей:</u> <b>{await get_count_users(db)}</b>\n"\
    f"🎮 <u>Всего игр:</u> <b>{await get_count_games(db)}</b>"


    await message.answer(content, reply_markup=admin_menu())