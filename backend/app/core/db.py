from sqlmodel import create_engine, Session, select

from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)
    # Or you can create specific tables
    # SQLModel.metadata.create_all(engine, tables=[User.__table__])
    with session.begin():
        pass