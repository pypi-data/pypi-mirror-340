import logging

# import sqlalchemy as sa
from sqlmodel import Session, select
from sqlalchemy.exc import NoResultFound, IntegrityError

# from sqlalchemy.sql import values
from uuid import UUID

from ceonmedia_db import models
from ceonmedia_db import schemas
from ceonmedia_db import errors
from ceonmedia_db import constants

# from db.engine import SessionLocal


logger = logging.getLogger(constants.LOGGER_NAME)


def delete(session: Session, project_uuid: UUID):
    project_to_delete = (
        session.query(models.ProjectTbl)
        .filter(models.ProjectTbl.id == project_uuid)
        .first()
    )
    session.delete(project_to_delete)
    session.commit()
    logger.info("Deleted project: %s", project_uuid)


def create(session: Session, project_create: schemas.ProjectCreate):
    logger.info(f"Creating project with project_create:\n{project_create}")
    new_project = models.ProjectTbl(**project_create.model_dump())
    logger.info(f"Adding project model to db:\n{new_project}")
    session.add(new_project)
    logger.info("Commiting changes to db...")
    session.commit()
    return new_project


def get(session: Session, project_uuid: UUID) -> models.ProjectTbl:
    stmt = select(models.ProjectTbl).where(models.ProjectTbl.id == project_uuid)
    try:
        got_project = session.execute(stmt).scalar_one()
    except NoResultFound as e:
        raise errors.NotFoundInDBError(f"Project {project_uuid} not found in db: {e}")
    return got_project


def get_proj_inputs(session: Session, project_uuid: UUID):
    stmt = select(models.ProjectTbl).where(models.ProjectTbl.id == project_uuid)
    try:
        got_project = session.execute(stmt).scalar_one()
    except NoResultFound as e:
        raise errors.NotFoundInDBError(f"Project {project_uuid} not found in db: {e}")
    proj_inputs = got_project.proj_inputs
    return proj_inputs


def get_all(session: Session):
    # TODO implement skip/pagination
    # TODO only return jobs belonging to user id
    logger.warning("TODO implement skipping/pagination for get_all projects")
    stmt = select(models.ProjectTbl).order_by(models.ProjectTbl.title)
    result = session.execute(stmt).scalars().all()
    return result


def update(session: Session, proj_uuid: UUID, **values):
    project = session.get(models.ProjectTbl, proj_uuid)
    if not project:
        logger.warning("-- PROJECT NOT FOUND: %s --", proj_uuid)
        return None
    logger.info(f"Got from DB project.id({project.id}): {project.title}")
    logger.info(f"Got values: {values}")
    # project.update(**values)
    # stmt = (
    #     sa.update(models.ProjectTbl)
    #     .where(models.ProjectTbl.id == proj_uuid)
    #     .values(**values)
    # )
    project.sqlmodel_update(values)
    session.add(project)
    # db.execute(stmt)
    # rowcount = result.rowcount
    # logger.info(f"update project result: {result}")
    # logger.info(f"update project rowcount: {rowcount}")
    session.commit()
    return project


def upsert(db: Session, proj_id: UUID, **values):
    logger.info("Got values to upsert: %s", values)
    new_project = models.ProjectTbl(id=proj_id, **values)
    logger.info("Cteated new_project: %s", new_project)
    try:
        db.merge(new_project)
        db.commit()
    except IntegrityError as e:
        errors.handle_sql_error(e)


"""
class Project:
    @classmethod
    def get(cls, db: Session, proj_uuid: UUID, raise_missing=False):
        stmt = select(ProjectTbl).where(ProjectTbl.id == proj_uuid)
        try:
            got_project = db.execute(stmt).scalar_one()
        except NoResultFound as e:
            if raise_missing:
                raise e
            return None
        return got_project

    @classmethod
    def get_all(cls, db: Session):
        # TODO only return jobs belonging to user id
        stmt = select(ProjectTbl).order_by(ProjectTbl.title)
        result = db.execute(stmt).scalars().all()
        return result

    @classmethod
    def get_proj_inputs(cls, db: Session, proj_uuid: UUID):
        stmt = select(ProjectTbl.proj_inputs).where(ProjectTbl.id == proj_uuid)
        got_project_inputs = db.execute(stmt).one()
        # return got_project["proj_inputs"]
        return got_project_inputs.proj_inputs

    @classmethod
    def create(cls, db: Session, **values):
        new_project = ProjectTbl(**values)
        db.add(new_project)
        db.commit()
        return new_project

    @classmethod
    def update(cls, db: Session, proj_uuid: UUID, **values):
        project = db.get(ProjectTbl, proj_uuid)
        if not project:
            logger.info("--NO PROJECT FOUND--")
            return None
        logger.info(f"Got from DB project.id({project.id}): {project.title}")
        logger.info(f"Got values: {values}")
        # project.update(**values)
        stmt = update(ProjectTbl).where(ProjectTbl.id == proj_uuid).values(**values)
        db.execute(stmt)
        # rowcount = result.rowcount
        # logger.info(f"update project result: {result}")
        # logger.info(f"update project rowcount: {rowcount}")
        db.commit()
        return project

    @classmethod
    def upsert(cls, db: Session, proj_uuid: UUID, **values):
        new_project = ProjectTbl(uuid=proj_uuid, **values)
        db.merge(new_project)
        db.commit()

    @classmethod
    def delete(cls, db: Session, proj_uuid: UUID):
        project = db.get(ProjectTbl, proj_uuid)
        logger.info(f"Got project for deletion: {project}")
        db.delete(project)
        db.commit()
        logger.info(f"Deleted proj({proj_uuid}) from db.")
        return proj_uuid
"""
