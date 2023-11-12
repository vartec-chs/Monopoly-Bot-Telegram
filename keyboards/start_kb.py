from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🪄 Создать игру",
                    callback_data="create_game"
                )
            ],
            [
                InlineKeyboardButton(
                    text="📄 Мои игры",
                    callback_data="my_games"
                )
            ],
            [
                InlineKeyboardButton(
                    text="▶️ Присоединиться к игре",
                    callback_data="join_game"
                )
            ]
        ]
    )