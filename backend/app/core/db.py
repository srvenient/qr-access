from sqlmodel import create_engine, Session, select

from app.api.role.domain.role_models import Role
from app.api.user.domain.user_models import User
from app.core import security
from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    role = session.exec(select(Role).where(Role.name == "admin")).first()
    if not role:
        role = Role(name="admin")
        session.add(role)
        session.commit()
        session.refresh(role)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = User(
            email=settings.FIRST_SUPERUSER,
            hashed_password=security.get_password_hash(settings.FIRST_SUPERUSER_PASSWORD),
            is_superuser=True,
            role_id=role.id,
        )
        session.add(user_in)
        session.commit()