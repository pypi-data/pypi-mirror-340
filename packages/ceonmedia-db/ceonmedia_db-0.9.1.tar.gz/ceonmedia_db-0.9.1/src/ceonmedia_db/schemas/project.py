# Pydantic models, renamed to 'schemas' to avoid being confused with sqlalchemy models.
from typing import Optional
from sqlmodel import SQLModel

# from pydantic import BaseModel, Field
from uuid import UUID


class ProjectCreate(SQLModel):
    title: str
    proj_inputs: list
    owner_uuid: Optional[UUID]
    description: Optional[str]
    uuid: Optional[UUID] = None

    class Config:
        from_attributes = True


# Remember to add Config orm_mode=True for classes which are reading db entries
# class Config:
#     orm_mode = True
