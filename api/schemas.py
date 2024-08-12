from pydantic import BaseModel


class WeatherInput(BaseModel):
    user_id: int


class UserProgressOutput(BaseModel):
    user_id: int
    progress: str