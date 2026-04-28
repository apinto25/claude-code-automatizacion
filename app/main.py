from fastapi import FastAPI

from app.database import Base, engine
from app.routers import appointments_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Appointments API")

app.include_router(appointments_router)
