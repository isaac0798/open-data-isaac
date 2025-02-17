from fastapi import FastAPI
from .database import get_db, init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    init_db()

@app.get("/")
async def root():
    return {"message": "Hello testd"}