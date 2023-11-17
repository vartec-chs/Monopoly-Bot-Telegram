from database.core import DataBase


async def delete_admin_by_tg_id(db: DataBase, tg_id: int) -> None:
    await db.admins_collection.delete_one({"tg_id": tg_id})