from database.core import DataBase
from database.requests.get import get_user_is_admin_by_tg_id, get_user_is_blocked_by_tg_id
from database.requests.create import add_new_admin
from database.requests.delete import delete_admin_by_tg_id



async def toggle_user_is_blocked_by_tg_id(db: DataBase, tg_id: str) -> None:
    await db.users_collection.update_one(
        {"tg_id": tg_id},
        {"$set": {"is_blocked": not await get_user_is_blocked_by_tg_id(db, tg_id)}}
    )

async def toggle_user_is_admin(db: DataBase, tg_id: int) -> None:
    if await get_user_is_admin_by_tg_id(db, tg_id):
        await delete_admin_by_tg_id(db, tg_id)
    else:
        await add_new_admin(db, tg_id)