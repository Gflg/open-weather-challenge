from sqlalchemy import Column, Integer, String, DateTime

from api.db.settings import Base


class User(Base):
    '''User model with its attributes.'''
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    weather_data = Column(String)
