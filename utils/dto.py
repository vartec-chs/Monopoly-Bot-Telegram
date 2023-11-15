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


