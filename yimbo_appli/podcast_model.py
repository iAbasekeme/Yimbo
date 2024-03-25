#!/usr/bin/python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from yimbo_appli.model import Base
from contextlib import contextmanager

# Create an engine to connect to the database
engine = create_engine('mysql+mysqldb://root:password@localhost:3306/podcast_database')

# Create a sessionmaker
SessionLocal = sessionmaker(bind=engine)

@contextmanager
def get_db():
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()

def create_tables():
    """Create all tables in the database."""
    Base.metadata.create_all(engine)
