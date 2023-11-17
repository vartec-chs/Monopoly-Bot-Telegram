from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field


PyObjectId = Annotated[str, BeforeValidator(str)]


class BaseDocument(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True



class UserIdAndNameDTO(BaseDocument):
    id: PyObjectId = Field(alias="_id", default=None)
    full_name: str


# class UserDto(BaseDocument):
#     id: PyObjectId = Field(alias="_id", default=None)
#     tg_id: int
#     active_game_id: int | None = Field(default=None)
#     all_games_id: list[int]
#     is_blocked: bool

#     def to_json(self): 
#         return self.model_dump(by_alias=True, exclude_none=True)