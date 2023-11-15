from aiogram import Bot

from database.core import DataBase
from database.requests.get import get_users_in_list_for_page

from utils.dto import UserIdAndNameDTO


async def get_users_list_with_names(db: DataBase, bot: Bot, page: int) -> list[UserIdAndNameDTO]:
    users_list = await get_users_in_list_for_page(db, page)

    users_list_with_names: list[UserIdAndNameDTO] = []

    for user in users_list:
        chat = await bot.get_chat(user["tg_id"])
        users_list_with_names.append(
            UserIdAndNameDTO(
                id = user["_id"], 
                full_name = chat.full_name
            )
        )
    return users_list_with_names