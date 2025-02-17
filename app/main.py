import json
from fastapi import FastAPI
from .database import get_db, init_db, drop_all_tables, insert_competition
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

@app.get("/process-competition")
async def root():
    config_path = Path("data-json/competitions.json")
    if config_path.exists():
        print('hi')
        with open(config_path) as f:
            competitions = json.load(f)
            db = get_db()
            
            for competition in competitions:
                insert_competition(
                    db,
                    competition_id=competition['competition_id'],
                    country_name=competition['country_name'],
                    competition_name=competition['competition_name'],
                    competition_gender=competition['competition_gender'],
                    competition_youth=competition['competition_youth'],
                    competition_international=competition['competition_international']
                )
                
        

@app.get("/reset-db")
async def reset_database():
    drop_all_tables()
    init_db()
    return {"message": "Database reset successfully"}