import datetime
import json
from api.db.actions import (
    create_user, update_user_weather_data, find_user_by_id
)
from api.tests.utils import delete_user


def test_create_user(get_session):
    '''Test if function is creating users properly.'''
    session = get_session
    id = 50000
    timestamp = datetime.datetime.now()
    weather_data = []
    
    user = create_user(session, id, timestamp, weather_data)
    user_weather_data = json.loads(user.weather_data)
    assert user.id == id
    assert user.timestamp == timestamp
    assert user_weather_data == weather_data
    
    delete_user(session, user)


def test_update_user(get_session):
    '''Test if function is updating users properly.'''
    session = get_session
    id = 50000
    timestamp = datetime.datetime.now()
    weather_data = []
    
    user = create_user(session, id, timestamp, weather_data)
    
    city_id = 100
    temperature = 250
    humidity = 30
    weather_data.append({
        'city_id': city_id,
        'temperature': temperature,
        'humidity': humidity
    })
    user = update_user_weather_data(session, user, weather_data)
    
    assert len(user.weather_data) > 0
    user_weather_data = json.loads(user.weather_data)
    assert user_weather_data[0]['city_id'] == city_id
    assert user_weather_data[0]['temperature'] == temperature
    assert user_weather_data[0]['humidity'] == humidity

    delete_user(session, user)


def test_get_user_by_id(get_session):
    '''Test if function is finding user by its ID properly.'''
    session = get_session
    id = 50000
    timestamp = datetime.datetime.now()
    weather_data = []
    
    user = create_user(session, id, timestamp, weather_data)
    user_weather_data = json.loads(user.weather_data)

    found_user = find_user_by_id(session, user.id)
    assert found_user is not None
    found_user_weather_data = json.loads(user.weather_data)

    assert found_user.id == user.id
    assert found_user.timestamp == user.timestamp
    assert found_user_weather_data == user_weather_data
    
    delete_user(session, user)
