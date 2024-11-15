import os
from collections.abc import Callable
from pathlib import Path
from time import sleep

from sqlalchemy import engine, orm, text

from backend.db.db_setup import session_context
from backend.utils.logger import get_logger

logger = get_logger(__name__)

def safe_try(func: Callable):
    try:
        func()
    except Exception as e:
        logger.error(f"Error calling '{func.__name__}': {e}")


def connect(session: orm.Session) -> bool:
    try:
        session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        logger.error(f"Error connecting to database: {e}")
        return False


def main():
    # Wait for database to connect
    max_retry = 10
    wait_seconds = 1

    with session_context() as session:
        while True:
            if connect(session):
                logger.info("Database connection established.")
                break

            logger.error(f"Database connection failed. Retrying in {wait_seconds} seconds...")
            max_retry -= 1

            sleep(wait_seconds)

            if max_retry == 0:
                raise ConnectionError("Database connection failed - exiting application.")

        # db = get_repositories(session)
        # if db.users:
        #     logger.debug("Database exists")
        # else:
        #     logger.info("Database contains no users, initializing...")
        #     default_user_init(db)


if __name__ == "__main__":
    main()
