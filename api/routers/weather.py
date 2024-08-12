import datetime
import json

from fastapi import APIRouter, Depends, HTTPException
from api.constants import CITIES_IDS
from api.db.actions import find_user_by_id
from api.db.settings import get_db
from api.worker import call_weather_api
from api.schemas import WeatherInput, UserProgressOutput
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/api/weather")
async def create_weather_data_for_user(
        weather_data: WeatherInput, db: Session = Depends(get_db)):
    timestamp = datetime.datetime.now()
    user_id = weather_data.user_id
    user = find_user_by_id(db, user_id)
    if user is not None:
        raise HTTPException(status_code=422, detail="User ID already exists")

    call_weather_api.delay(user_id, timestamp)
    response = {
        'user_id': user_id,
        'timestamp': timestamp,
        'status': 'in_progress'
    }

    return response


@router.get("/api/weather/{user_id}")
def get_progress_from_user(
        user_id: int, db: Session = Depends(get_db)) -> UserProgressOutput:
    user = find_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    weather_data = json.loads(user.weather_data)
    progress_percentage = (len(weather_data)/len(CITIES_IDS)) * 100
    return {
        'user_id': user_id,
        'progress': str(round(progress_percentage, 2)) + '%'
    }
