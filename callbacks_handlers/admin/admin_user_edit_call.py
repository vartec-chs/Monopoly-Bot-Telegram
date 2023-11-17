from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from config import ADMINS_ID

from database.core import DataBase
from database.requests.get import get_user_by_id
from database.requests.toggle import toggle_user_is_admin, toggle_user_is_blocked_by_tg_id

from filters.admin_filter import IsAdmin
from utils.text_builders import user_settings_text



router = Router()


@router.callback_query(F.data.startswith("admin_toggle_admin_"), IsAdmin())
async def admin_user_edit(callback: CallbackQuery, db: DataBase, bot: Bot):
    await callback.answer()

    user_id = callback.data.split("_")[3]

    user = await get_user_by_id(db, user_id)
    tg_id = user["tg_id"]


    if tg_id in ADMINS_ID:
        return await callback.message.answer(
            "❌ <b>Вы не можете взаимодействовать с админом выше вас!</b>"
            )
    if tg_id == callback.from_user.id:
        return await callback.message.answer(
            "❌ <b>Вы не можете изменить этот статус!</b>"
            )

    await toggle_user_is_admin(db, tg_id)

    await user_settings_text.user_settings_text_sender(
    user_settings_text.UserSenderData(
            user_id = user_id,
            tg_id = tg_id,
            bot = bot,
            db = db,
            callback = callback
        )
    )


@router.callback_query(F.data.startswith("admin_toggle_block_"), IsAdmin())
async def admin_user_edit_block(callback: CallbackQuery, db: DataBase, bot: Bot):
    await callback.answer()

    user_id = callback.data.split("_")[3]
    user = await get_user_by_id(db, user_id)
    tg_id = user["tg_id"]


    if tg_id in ADMINS_ID:
        return await callback.message.answer(
            "❌ <b>Вы не можете взаимодействовать с админом выше вас!</b>"
            )
    if tg_id == callback.from_user.id:
        return await callback.message.answer(
            "❌ <b>Вы не можете изменить этот статус!</b>"
            )

    await toggle_user_is_blocked_by_tg_id(db, tg_id)

    await user_settings_text.user_settings_text_sender(
    user_settings_text.UserSenderData(
            user_id = user_id,
            tg_id = tg_id,
            bot = bot,
            db = db,
            callback = callback
        )
    )
