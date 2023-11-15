from contextlib import suppress

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database.core import DataBase
from database.requests.get import get_user_by_id, get_count_users, SKIP

from filters.admin_filter import IsAdmin
from utils.other import get_users_list_with_names
from keyboards.admin_kb import UsersListPagination, admin_users_list_menu

router = Router(name=__name__)




@router.callback_query(F.data == "admin_games_list", IsAdmin())
async def admin_games(callback: CallbackQuery):
    await callback.answer()



@router.callback_query(F.data.startswith("admin_users_list_"), IsAdmin())
async def admin_user_info(callback: CallbackQuery, db: DataBase, bot: Bot):
    await callback.answer()

    _id = callback.data.split("_")[3]
    user = await get_user_by_id(db, _id)

    chat = await bot.get_chat(user["tg_id"])

    user_id = user["tg_id"]

    content = f"👤 <b>Информация о пользователе:</b>\n\n"\
    f"🆔 <b>ID:</b> <i>{user_id}</i>\n"\
    f"👤 <b>Имя:</b> <i>{chat.full_name}</i>\n"\
    

    await callback.message.edit_text(content)
      



@router.callback_query(F.data == "admin_users_list", IsAdmin())
async def admin_users_list(callback: CallbackQuery, db: DataBase, bot: Bot):
    await callback.answer()

    users_list_with_names = await get_users_list_with_names(db, bot, 0)
    page_count = int(await get_count_users(db) / SKIP)

    content = "👥 <b>Все пользователи:</b>\n\n"\
    f"📄 <i>Страница</i> <u>1</u> <i>из</i> <u>{page_count}</u>"

    await callback.message.edit_text(
        content,
        reply_markup=admin_users_list_menu(users_list_with_names)
    )


@router.callback_query(UsersListPagination.filter())
async def users_list_pagination(
    call: CallbackQuery, callback_data: UsersListPagination, db: DataBase, bot: Bot
    ):

    current_page = int(callback_data.page)
    page_count = int(await get_count_users(db) / SKIP)

    if callback_data.action == "prev":
        page = current_page - 1 if current_page > 0 else 0
    elif callback_data.action == "next":
        page = current_page + 1 if current_page < (page_count - 1) else current_page

    users_list_with_names = await get_users_list_with_names(db, bot, page)

    with suppress(TelegramBadRequest):

        constent = f"👥 <b>Все пользователи:</b>\n\n"\
        f"📄 <i>Страница</i> <u>{page + 1}</u> <i>из</i> <u>{page_count}</u>"

        await call.message.edit_text(
            constent,
            reply_markup=admin_users_list_menu(users_list_with_names, page)
        )
    await call.answer()