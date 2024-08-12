from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from api.constants import DATABASE_NAME


SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DATABASE_NAME}.db"

engine = create_engine(
  SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    '''Create session from database.'''
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()