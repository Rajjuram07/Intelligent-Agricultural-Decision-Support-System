from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Float
)

from sqlalchemy.orm import declarative_base

from datetime import datetime


# =========================================================
# BASE
# =========================================================
Base = declarative_base()


# =========================================================
# CHAT HISTORY
# =========================================================
class ChatHistory(Base):

    __tablename__ = "chat_history"

    id = Column(
        Integer,
        primary_key=True
    )

    role = Column(
        String
    )

    message = Column(
        Text
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================================================
# ACTIVITY HISTORY
# =========================================================
class ActivityHistory(Base):

    __tablename__ = "activity_history"

    id = Column(
        Integer,
        primary_key=True
    )

    module = Column(
        String
    )

    query = Column(
        Text
    )

    response = Column(
        Text
    )

    retrieval_engine = Column(
        String
    )

    language = Column(
        String
    )

    ai_temperature = Column(
        Float
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )