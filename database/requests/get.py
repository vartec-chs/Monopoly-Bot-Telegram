from bson import ObjectId
from database.core import DataBase


SKIP = 1 # for pagination users in admin menu ||| after 8 users in one page


async def get_count_users(db: DataBase) -> int:
    return await db.users_collection.count_documents({})

async def get_count_games(db: DataBase) -> int:
    return await db.games_collection.count_documents({})


async def get_user_by_id(db: DataBase, _id: str) -> dict:
    return await db.users_collection.find_one({"_id": ObjectId(_id)})


async def get_user_exists(db: DataBase, tg_id: int) -> bool:
    return await db.users_collection.count_documents({"tg_id": tg_id}) == 1


async def get_user_is_blocked(db: DataBase, tg_id: int) -> bool:
    return await db.users_collection.count_documents({"tg_id": tg_id, "is_blocked": True}) == 1


async def get_user_is_admin(db: DataBase, tg_id: int) -> bool:
    return await db.admins_collection.count_documents({"tg_id": tg_id}) == 1


async def get_all_users(db: DataBase) -> list:
    return await db.users_collection.find({}, {"tg_id": 1, "_id": 1}).to_list(None)


async def get_users_in_list_for_page(db: DataBase, page: int) -> list:
    return await db.users_collection.find(
        {}, 
        {
            "tg_id": 1, 
            "_id": 1
        }
        ).skip(page * SKIP).limit(SKIP).to_list(None)