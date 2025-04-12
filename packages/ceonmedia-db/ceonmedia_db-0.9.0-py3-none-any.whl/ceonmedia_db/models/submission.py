from uuid import uuid4, UUID
from datetime import date, timedelta, datetime

from sqlmodel import SQLModel, Field

import sqlalchemy as sa


def get_valid_until():
    valid_until = date.today() + timedelta(days=30)
    return valid_until


class SubmissionTbl(SQLModel, table=True):
    __tablename__ = "submission"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        sa_column_kwargs={"server_default": sa.text("gen_random_uuid()")},
        nullable=False,
        index=True,
    )
    user_account_id: UUID = Field(foreign_key="user.id", ondelete="CASCADE")
    project_id: UUID = Field(foreign_key="project.id", ondelete="CASCADE")
    validated: bool = Field(
        default=False,
        sa_column_kwargs={
            "server_default": "false",
        },
        nullable=False,
    )
    expires_at: datetime = Field(default_factory=get_valid_until)
    created_at: datetime | None = Field(
        default=None, nullable=False, sa_column_kwargs={"server_default": sa.func.now()}
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now(), "onupdate": sa.func.now()},
    )
    # project: "ProjectTbl" = Relationship()
