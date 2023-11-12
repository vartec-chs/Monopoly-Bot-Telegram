from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase

from config import GAMES_COLLECTION, USERS_COLLECTION, ADMINS_COLLECTION

class DataBase:
    def __init__(self, url: str, db_name: str) -> None:
        self.__client: AsyncIOMotorClient = AsyncIOMotorClient(url)
        self.__db: AsyncIOMotorDatabase = self.__client[db_name]

    @property
    def db(self) -> AsyncIOMotorDatabase:
        return self.__db
    
    @property
    def games_collection(self) -> AsyncIOMotorCollection:
        return self.__db[GAMES_COLLECTION]
    
    @property
    def users_collection(self) -> AsyncIOMotorCollection:
        return self.__db[USERS_COLLECTION]
    
    @property
    def admins_collection(self) -> AsyncIOMotorCollection:
        return self.__db[ADMINS_COLLECTION]


    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection:
        return self.__db[collection_name]
    

