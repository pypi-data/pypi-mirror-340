import logging
from uuid import UUID
from sqlalchemy import select
from sqlmodel import Session

from ceonmedia_db.models.submission import SubmissionTbl
from ceonmedia_db import constants

logger = logging.getLogger(constants.LOGGER_NAME)


def create(
    db,
    user_id: str,
    project_id: str,
    submission_id: str | None,
):
    logger.info(f"Received values: {submission_id=}, {user_id=}, {project_id=}")
    new_submission = SubmissionTbl(
        user_account_id=user_id,
        project_id=project_id,
        id=submission_id,
    )
    db.add(new_submission)
    db.commit()
    return new_submission


def get(db: Session, submission_id: UUID):
    # TODO switch to ORM workflow (is select ORM?)
    stmt = select(SubmissionTbl).where(SubmissionTbl.id == submission_id)
    got_submission = db.execute(stmt).scalars().one()
    return got_submission


# def get_by_job_id(db: Session, job_id: UUID) -> SubmissionTbl:
#     stmt = select(SubmissionTbl).where(SubmissionTbl.job_id == job_id)
#     got_submission = db.execute(stmt).scalars().one()
#     return got_submission
