from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


from utils.dto import UserIdAndNameDTO


class UsersListPagination(CallbackData, prefix="admin"):
    action: str
    page: int


def admin_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👥 Пользователи",
                    callback_data="admin_users_list"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎮 Игры",
                    callback_data="admin_games_list"
                )
            ]
        ]
    )


def admin_users_list(page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="⬅️",
            callback_data=UsersListPagination(action="prev", page=page).pack()
        ),
        InlineKeyboardButton(
            text="➡️",
            callback_data=UsersListPagination(action="next", page=page).pack()
        ),
        width=2
    )
    return builder.as_markup()


def users_list_menu(users: list[UserIdAndNameDTO]):
    builder = InlineKeyboardBuilder()

    for user in users:
        builder.row(
            InlineKeyboardButton(
                text=user.full_name,
                callback_data=f"admin_users_list_{user.id}"
            ),
            width=2
        )
    
    return builder.as_markup()


def admin_users_list_menu(users: list[UserIdAndNameDTO], page: int = 0) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for user in users:
        builder.row(
            InlineKeyboardButton(
                text=user.full_name,
                callback_data=f"admin_users_list_{user.id}"
            )
        )
        
    builder.row(
        InlineKeyboardButton(
            text="⬅️",
            callback_data=UsersListPagination(action="prev", page=page).pack()
        ),
        InlineKeyboardButton(
            text="➡️",
            callback_data=UsersListPagination(action="next", page=page).pack()
        ),
        width=2
    )
    return builder.as_markup()


def admin_user_settings_menu(user_id: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🪄 Переключить статус админа",
                    callback_data=f"admin_toggle_admin_{user_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔒 Переключит сатус блокировки",
                    callback_data=f"admin_toggle_block_{user_id}"
                ),   
            ],
            [
                InlineKeyboardButton(
                    text="🗑 Удалить пользователя",
                    callback_data=f"admin_delete_user_{user_id}"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="↩️ Назад",
                    callback_data="admin_users_list"
                ),
            ]
            ]
    )