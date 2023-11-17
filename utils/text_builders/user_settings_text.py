from dataclasses import dataclass
from aiogram import Bot

from aiogram.types import Chat, CallbackQuery

from database.core import DataBase
from database.requests.get import get_user_is_blocked_by_tg_id, get_user_is_admin_by_tg_id
from keyboards.admin_kb import admin_user_settings_menu

@dataclass
class UserData:
    user_id: str
    tg_id: int
    chat: Chat
    db: DataBase


@dataclass
class UserSenderData:
    user_id: str
    tg_id: int
    db: DataBase
    bot: Bot
    callback: CallbackQuery





async def user_settings_text_builder(user_data: UserData) -> str:

    db = user_data.db

    user_is_bloked = await get_user_is_blocked_by_tg_id(db, user_data.tg_id)
    user_is_bloked_emoji = "🔴" if user_is_bloked else "🟢"

    user_is_admin = await get_user_is_admin_by_tg_id(db, user_data.tg_id)
    user_is_admin_emoji = "👑" if user_is_admin else "🔴"

    content = \
    "👤 <b>Информация о пользователе:</b>\n\n"\
    f"🆔 <b>ID:</b> <i><u>{user_data.tg_id}</u></i>\n"\
    f"👤 <b>Имя:</b> <i>{user_data.chat.first_name}</i>\n"\
    f"👤 <b>Фамилия:</b> <i>{user_data.chat.last_name}</i>\n"\
    f"😶‍🌫️ <b>Никнейм:</b> <i>{user_data.chat.username}</i>\n"\
    f"🚫 Статуст блокировки: {user_is_bloked_emoji}\n"\
    f"🛡️ Статус админа: {user_is_admin_emoji}"

    return content


async def user_settings_text_sender(user_sender_data: UserSenderData) -> str:

    chat = await user_sender_data.bot.get_chat(user_sender_data.tg_id)
    
    content = await user_settings_text_builder(
        UserData(
            user_id = user_sender_data.user_id,
            tg_id = user_sender_data.tg_id,
            chat = chat,
            db=user_sender_data.db
        )
    )
    
    await user_sender_data.callback.message.edit_text(
        content, 
        reply_markup=admin_user_settings_menu(
            user_sender_data.user_id
        )
        )