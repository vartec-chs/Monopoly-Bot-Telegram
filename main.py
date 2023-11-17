import sys
import asyncio
from os import getenv

from dotenv import load_dotenv
from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.types.bot_command import BotCommand

from config import DB_NAME, ADMINS_ID

from database.core import DataBase
from database.requests.get import get_user_is_admin_by_tg_id
from database.requests.create import add_new_admin

from middlewares.is_blocked_user import IsUserBlocked

from command_handlers import start_cmd, admin_cmd
from callbacks_handlers.admin import admin_call, admin_user_edit_call



async def main() -> None:
    load_dotenv(".env")

    bot = Bot(token=getenv("BOT_TOKEN"), parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    dp.message.middleware(IsUserBlocked())
    dp.callback_query.middleware(IsUserBlocked())

    dp.include_routers(
        start_cmd.router,
        admin_cmd.router,
        admin_call.router,
        admin_user_edit_call.router
    )

    db = DataBase(url=getenv("DB_URL"), db_name=DB_NAME)

    await add_admins(db)

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    await bot.set_my_commands([
        BotCommand(
            command="start",
            description="👋 Стартовое меню"
        ),
        BotCommand(
            command="join",
            description="➡️ Войти в игру"
        ),
        BotCommand(
            command="game_menu",
            description="⚙️ Игровое меню"
        ),
        BotCommand(
            command="admin",
            description="🛡️ Админ меню"
        )
    ])

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, db=db)



async def on_startup() -> None:
    logger.info("Bot started!")


async def on_shutdown() -> None:
    logger.warning("Bot stopped!")


async def add_admins(db: DataBase) -> None:
    for admin_id in ADMINS_ID:
        if not await get_user_is_admin_by_tg_id(db, admin_id):
            await add_new_admin(db, admin_id)


if __name__ == "__main__":
    logger.add(
        sys.stderr,
        colorize=True,
        format="{time} {level} {message}",
        filter="my_module",
        level="INFO",
    )
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass