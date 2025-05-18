# backend/main.py
from fastapi import FastAPI
from .routers import events, users, bookings
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TickeTaka - Event Ticketing System",
    description="Event management with QR tickets, demand forecasting, and recommendations",
    version="1.0.0"
)

app.include_router(events.router)
app.include_router(users.router)
app.include_router(bookings.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to TickeTaka API!"}
