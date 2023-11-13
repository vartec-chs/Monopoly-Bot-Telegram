from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from bson import ObjectId

from database.core import DataBase
from database.requests.get import get_all_users, get_user_by_id

from filters.admin_filter import IsAdmin
from utils.user_dto import UserDTO
from keyboards.admin_kb import admin_users_list, users_list_menu

router = Router(name=__name__)

# 6797214853 bot id

@router.callback_query(F.data == "admin_users_list", IsAdmin())
async def admin_users(callback: CallbackQuery, db: DataBase, bot: Bot):
    await callback.answer()

    users = await get_all_users(db)

    users_names: list[UserDTO] = []

    for user in users:
        chat = await bot.get_chat(user["tg_id"])
        users_names.append(UserDTO(user["_id"], chat.full_name))

    await callback.message.edit_text(
        "👥 <b>Все пользователи:</b>", 
        reply_markup=users_list_menu(users_names)
        )



@router.callback_query(F.data == "admin_games_list", IsAdmin())
async def admin_games(callback: CallbackQuery):
    await callback.answer()



@router.callback_query(F.data.startswith("admin_users_list_"), IsAdmin())
async def admin_users_list_handler(callback: CallbackQuery, db: DataBase, bot: Bot):
    await callback.answer()

    _id = callback.data.split("_")[3]
    user = await get_user_by_id(db, _id)

    print(user)

    chat = await bot.get_chat(user["tg_id"])

    user_id = user["tg_id"]

    content = f"👤 <b>Информация о пользователе:</b>\n\n"\
    f"🆔 <b>ID:</b> <i>{user_id}</i>\n"\
    f"👤 <b>Имя:</b> <i>{chat.full_name}</i>\n"\
    

    await callback.message.edit_text(content)
      