from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


from utils.user_dto import UserDTO


class Pagination(CallbackData, prefix="admin"):
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
            callback_data=Pagination(action="prev", page=page).pack()
        ),
        InlineKeyboardButton(
            text="➡️",
            callback_data=Pagination(action="next", page=page).pack()
        ),
        width=2
    )
    return builder.as_markup()


def users_list_menu(users: list[UserDTO]):
    builder = InlineKeyboardBuilder()

    for user in users:
        builder.row(
            InlineKeyboardButton(
                text=user.full_name,
                callback_data=f"admin_users_list_{user._id}"
            ),
            width=2
        )
    
    return builder.as_markup()


