from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm.session import Session

from core.settings import get_app_settings
from db.database import get_db
from sqlalchemy.orm import Session
from db.models import User, Chore
from schema.schemas import UserSchema, UserCreateSchema

router = APIRouter(prefix="/about")

@router.get("")
def get_app_info():
    """Get general application information"""
    settings = get_app_settings()

    return settings.model_dump_json(
            indent=4,
            exclude={
                "SECRET",
                "SFTP_PASSWORD",
                "SFTP_USERNAME",
                "DB_URL",  # replace by DB_URL_PUBLIC for logs
                "DB_PROVIDER",
                "SMTP_USER",
                "SMTP_PASSWORD",
            },
        )

@router.get("/startup-info")
def get_startup_info(db: Session = Depends(get_db)):
    """returns helpful startup information"""
    settings = get_app_settings()

    is_first_login = False
    if db.query(User).filter_by(email=settings._DEFAULT_EMAIL).count() > 0:
        is_first_login = True

    return {
        "is_first_login": is_first_login
    }

@router.get("/num-users")
def get_num_users(db: Session = Depends(get_db)):
    """returns the number of users in the database"""
    return db.query(User).count()