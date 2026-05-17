from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Text,
    DateTime
)

from sqlalchemy.ext.declarative import (
    declarative_base
)

from sqlalchemy.orm import (
    sessionmaker
)

from sqlalchemy import create_engine

from datetime import datetime


# =========================================================
# DATABASE
# =========================================================
DATABASE_URL = "sqlite:///krishimitra_logs.db"

engine = create_engine(
    DATABASE_URL
)

SessionLocal = sessionmaker(
    bind=engine
)

Base = declarative_base()


# =========================================================
# AGRICULTURE LOG TABLE
# =========================================================
class AgricultureLog(Base):

    __tablename__ = "agriculture_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(Text)

    response = Column(Text)

    crop = Column(String)

    state = Column(String)

    prediction = Column(Float)

    heat_risk = Column(String)

    rainfall_risk = Column(String)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# =========================================================
# CREATE TABLES
# =========================================================
Base.metadata.create_all(
    bind=engine
)


# =========================================================
# SAVE LOG
# =========================================================
def save_agriculture_log(
    question,
    response,
    crop,
    state,
    prediction,
    heat_risk,
    rainfall_risk
):

    db = SessionLocal()

    log = AgricultureLog(
        question=question,
        response=response,
        crop=crop,
        state=state,
        prediction=prediction,
        heat_risk=heat_risk,
        rainfall_risk=rainfall_risk
    )

    db.add(log)

    db.commit()

    db.close()