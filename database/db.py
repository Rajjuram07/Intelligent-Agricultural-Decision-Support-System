from database.models import Base

from sqlalchemy import create_engine

from utils.config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)


DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)


engine = create_engine(
    DATABASE_URL
)

# =========================================================
# CREATE DATABASE TABLES
# =========================================================
Base.metadata.create_all(
    bind=engine
)