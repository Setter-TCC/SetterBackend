from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.configs.environment import get_environment_variables

env = get_environment_variables()

Engine = create_engine(env.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=Engine)


def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()
