import json
from fastapi import FastAPI
from .database import get_db, init_db, drop_all_tables, insert_competition, get_competitions, insert_season, get_seasons_for_competition, insert_match, get_matches_in_season
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

@app.get("/process-matches")
async def root():
    db = get_db()
    competitions = get_competitions(db)
    
    for competition in competitions:
        seasons = get_seasons_for_competition(db, competition_id=competition['id'])
        
        for season in seasons:
            matches_path = Path(f"data-json/matches/{competition['id']}/{season['id']}.json")
            if matches_path.exists():
                with open(matches_path) as f:
                    matches = json.load(f)
                    
                    for match in matches:
                        insert_match(
                            db=db,
                            match_id=match['match_id'],
                            season_id=season['id']
                        )
                        
@app.get("/process-events")
async def root():
    db = get_db()
    competitions = get_competitions(db)
    
    for competition in competitions:
        seasons = get_seasons_for_competition(db, competition_id=competition['id'])
        
        for season in seasons:
            matches = get_matches_in_season(db, season['id'])
            
            for match in matches:
                event_path = Path(f"data-json/events/{match['id']}.json")
                if event_path.exists():
                    with open(event_path) as f:
                        events = json.load(f)
                        
                        print(events)
                
                        
            


@app.get("/process-seasons")
async def root():
    config_path = Path("data-json/competitions.json")
    if config_path.exists():
        with open(config_path) as f:
            competitions = json.load(f)
            db = get_db()
            
            for competition in competitions:
                insert_season(
                    db=db,
                    competition_id=competition['competition_id'],
                    season_id=competition['season_id'],
                    season_name=competition['season_name']
                )

@app.get("/process-competition")
async def root():
    config_path = Path("data-json/competitions.json")
    if config_path.exists():
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