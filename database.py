from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Settings

"""
Connect Database and generate db variable to communicate with models and perform query.
"""

engine = create_engine(Settings().DB_URL, echo=True)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()


def get_db():
    """
    Create db Session to use in models for database calls.
    :return: db Object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
