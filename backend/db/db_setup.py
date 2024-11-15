from collections.abc import Generator
from contextlib import contextmanager

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from backend.db.models import Base

DB_ENGINE="sqlite"

def sql_global_init(db_url: str):
    connect_args = {}
    if "sqlite" in db_url:
        connect_args["check_same_thread"] = False

    engine = sa.create_engine(db_url, echo=False, connect_args=connect_args, pool_pre_ping=True, future=True)

    Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

    return SessionLocal, engine


db_url = ""
if DB_ENGINE == "sqlite":
    db_url = f"sqlite:///./gopherden.db"
else:
    raise ValueError(f"Unsupported database engine: {DB_ENGINE}")
SessionLocal, engine = sql_global_init(db_url)  # type: ignore


@contextmanager
def session_context() -> Session:
    """
    session_context() provides a managed session to the database that is automatically
    closed when the context is exited. This is the preferred method of accessing the
    database.

    Note: use `generate_session` when using the `Depends` function from FastAPI
    """
    global SessionLocal
    sess = SessionLocal()
    try:
        yield sess
    finally:
        sess.close()


def generate_session() -> Generator[Session, None, None]:
    """
    WARNING: This function should _only_ be called when used with
    using the `Depends` function from FastAPI. This function will leak
    sessions if used outside of the context of a request.

    Use `with_session` instead. That function will allow you to use the
    session within a context manager
    """
    global SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
