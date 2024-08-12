import datetime
import json
from typing import List
from sqlalchemy.orm import Session
from api.db.models import User


def find_user_by_id(db: Session, id: int) -> User:
    '''Return an user matching the given ID.'''
    return db.query(User).filter(User.id == id).first()


def create_user(
        db: Session, user_id: int, timestamp: datetime.datetime, weather_data: List) -> User:
    '''Create a new user on database with new properties.'''
    user = User(
        id=user_id,
        timestamp=timestamp,
        weather_data=json.dumps(weather_data)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user_weather_data(
        db: Session, user: User, weather_data: List) -> User:
    '''Update weather_data from an existing user on database.'''
    user.weather_data = json.dumps(weather_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
