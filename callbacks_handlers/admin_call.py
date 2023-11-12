from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from database.core import DataBase
from database.requests.get import get_all_users, get_user_by_id

from filters.admin_filter import IsAdmin

router = Router(name=__name__)

# 6797214853 bot id

@router.callback_query(F.data == "admin_users_list", IsAdmin())
async def admin_users(callback: CallbackQuery, db: DataBase, bot: Bot):
    await callback.answer()

    users = await get_all_users(db)

    # users_names = []

    # count = 0
    # for user in users:
    #     count += 1
        # chat = await bot.get_chat(user["tg_id"])
        # users_names.append(f"{count} - {chat.full_name}\n")

    

    # content = "".join(users_names)

    # await callback.message.edit_text(content)

@router.callback_query(F.data == "admin_games_list", IsAdmin())
async def admin_games(callback: CallbackQuery):
    await callback.answer()