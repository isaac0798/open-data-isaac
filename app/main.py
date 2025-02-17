import json
from fastapi import FastAPI
from .database import get_db, init_db, drop_all_tables
import logging
from pathlib import Path

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

@app.get("/process")
async def root():
    config_path = Path("data-json/competitions.json")
    if config_path.exists():
        print('hi')
        with open(config_path) as f:
            return json.load(f)
        

@app.get("/reset-db")
async def reset_database():
    drop_all_tables()
    init_db()
    return {"message": "Database reset successfully"}