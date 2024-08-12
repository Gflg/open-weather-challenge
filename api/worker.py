import sys

sys.path.append('..')

import os
import requests

from celery import Celery
from api.db.actions import (
    create_user, update_user_weather_data
)
from api.db.settings import engine
from api.constants import CITIES_IDS, APP_ID
from sqlalchemy.orm import Session


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")


def find_weather_data(city_id: int):
    '''Function to call Open Weather API for a specific city ID.'''
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={APP_ID}')
        response = response.json()
    except Exception as e:
        raise e
    return response


def insert_weather_data_from_cities(
        session,
        user,
        all_weather_data,
        cities_ids):
    '''Function to insert data from cities on the given user.'''

    all_weather_data = all_weather_data if all_weather_data is not None else []

    for city_id in cities_ids:
        response_json = find_weather_data(city_id)
        weather_data = {
            'city_id': city_id,
            'temperature': response_json['main']['temp'],
            'humidity': response_json['main']['humidity']
        }
        all_weather_data.append(weather_data)

        user = update_user_weather_data(session, user, all_weather_data)

    return user, all_weather_data


@celery.task(name="call_weather_api")
def call_weather_api(*args):
    '''Celery task to call model and save its data linked to current user.'''
    user_id = args[0]
    timestamp = args[1]
    cities_ids = CITIES_IDS if len(args) <= 2 else args[2]
    last_saved_json = []
    user = None

    with Session(engine) as session:
        user = create_user(session, user_id, timestamp, last_saved_json)
        user, last_saved_json = insert_weather_data_from_cities(
            session, user, last_saved_json, cities_ids
        )