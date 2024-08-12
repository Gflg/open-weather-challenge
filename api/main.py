import sys

sys.path.append('..')

from fastapi import FastAPI
from api.db.settings import engine, Base
from api.routers import weather

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(weather.router)
