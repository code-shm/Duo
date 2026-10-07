"""Shared FastAPI dependencies."""

from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from .database import get_db
from .errors import api_error
from .models import User

DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(db: DbSession) -> User:
    """Authentication is out of scope: every request acts as the default learner."""
    user = db.scalar(select(User).where(User.is_bot.is_(False)).order_by(User.id))
    if user is None:
        raise api_error(503, "not_seeded", "The database has not been seeded yet.")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
