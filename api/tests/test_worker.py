import datetime
import json
from api.constants import CITIES_IDS
from api.db.actions import create_user, find_user_by_id
from api.worker import (
    call_weather_api,
    find_weather_data,
    insert_weather_data_from_cities
)
from api.tests.utils import delete_user


def test_find_weather_data():
    city_id = 3443631
    response = find_weather_data(city_id)
    assert isinstance(response, dict)
    
    main_keys = [
        "coord",
        "weather",
        "base",
        "main",
        "visibility",
        "wind",
        "clouds",
        "dt",
        "sys",
        "timezone",
        "id",
        "name",
        "cod"
    ]
    for key in main_keys:
        assert key in response
    assert response["id"] == city_id


def test_insert_weather_data_from_cities(get_session):
    session = get_session
    id = 50000
    timestamp = datetime.datetime.now()
    weather_data = []
    
    user = create_user(session, id, timestamp, weather_data)
    cities_ids = CITIES_IDS[:2]
    user, _ = insert_weather_data_from_cities(
        session, user, weather_data, cities_ids
    )

    user_weather_data = json.loads(user.weather_data)
    assert len(user_weather_data) == len(cities_ids)
    for index in range(len(user_weather_data)):
        assert 'city_id' in user_weather_data[index]
        assert user_weather_data[index]['city_id'] == cities_ids[index]
    
    delete_user(session, user)


def test_call_weather_api(get_session):
    session = get_session
    id = 50000
    timestamp = datetime.datetime.now()
    cities_ids = CITIES_IDS[:2]
    call_weather_api(id, timestamp, cities_ids)

    user = find_user_by_id(session, id)
    assert user.id == id

    user_weather_data = json.loads(user.weather_data)
    assert len(user_weather_data) == len(cities_ids)
    for index in range(len(user_weather_data)):
        assert 'city_id' in user_weather_data[index]
        assert user_weather_data[index]['city_id'] == cities_ids[index]
    
    delete_user(session, user)