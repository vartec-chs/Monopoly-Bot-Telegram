from loguru import logger

from database.core import DataBase



async def add_new_admin(db: DataBase, tg_id: int) -> None:

    admin_data = {
        "tg_id": tg_id
    }

    await db.admins_collection.insert_one(admin_data)

    logger.info(f"Added new admin with telegram id: {tg_id}")

async def add_new_user(db: DataBase, tg_id: int) -> None:

    user_data = {
        "tg_id": tg_id,
        "active_game_id": None,
        "all_games_id": [],
        "is_blocked": False
    }

    await db.users_collection.insert_one(user_data)

    logger.info(f"Added new user with telegram id: {tg_id}")