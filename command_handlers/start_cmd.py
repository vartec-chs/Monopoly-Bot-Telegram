from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from database.core import DataBase
from database.requests.create import add_new_user

from filters.user_filter import IsUserExists
from keyboards.start_kb import start_menu


router = Router(name=__name__)


# If user exists and deep link exists

@router.message(CommandStart(deep_link=True), IsUserExists())
async def start_user_with_deep_link(message: Message):
    await message.delete()

    game_id = int(message.text.split(" ")[1])

    await message.answer(f"Id of game: {game_id}")


@router.message(CommandStart(), IsUserExists())
async def start_user(message: Message):
    await message.delete()

    await message.answer("🖥️ <b>Стартовое меню:</b>", reply_markup=start_menu())


# If user dont exists and deep link exists


@router.message(CommandStart(deep_link=True))
async def start_not_user_exists_and_with_deep_link(message: Message, db: DataBase):
    await message.delete()

    tg_id = message.from_user.id
    await add_new_user(db, tg_id)

    game_id = int(message.text.split(" ")[1])

    await message.answer(
        f"Привет, <b>{message.from_user.full_name}</b>! 👋 \n\n"\
        f"Вы хотите перейти в эту игру? {game_id}"\
        )



@router.message(CommandStart())
async def start_not_user_exists(message: Message, db: DataBase):
    await message.delete()

    tg_id = message.from_user.id
    await add_new_user(db, tg_id)

    content = f"👋 Привет <b>{message.from_user.first_name}</b>!\n\n" \
    "<u><i>Выбери что-то из меню ниже</i></u> ⬇️"

    await message.answer(content, reply_markup=start_menu())