import sqlite3
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
DATABASE_PATH = Path("/data/app.db")

def get_db():
    """Get database connection with row factory"""
    DATABASE_PATH.parent.mkdir(exist_ok=True)  # Ensure data directory exists
    conn = sqlite3.connect(str(DATABASE_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database and create tables if they don't exist"""
    logger.info(f"Initializing database at {DATABASE_PATH}")
    db = get_db()
    
    try:
        # Create your tables here
        db.execute("""
            CREATE TABLE IF NOT EXISTS competition (
                id INTEGER PRIMARY KEY,
                country_name TEXT,
                competition_name TEXT,
                competition_gender TEXT,
                competition_youth INTEGER,
                competition_international INTEGER
            )
        """)
        
        db.execute("""
            CREATE TABLE IF NOT EXISTS season (
                id INTEGER PRIMARY KEY,
                competition_id INTEGER,
                name TEXT,
                FOREIGN KEY(competition_id) REFERENCES competition(id)
            )
        """)
        
        db.execute("""
            CREATE TABLE IF NOT EXISTS match (
                id INTEGER PRIMARY KEY,
                season_id INTEGER,
                FOREIGN KEY(season_id) REFERENCES season(id)
            )
        """)
        
        db.execute("""
            CREATE TABLE IF NOT EXISTS match_event (
                id TEXT PRIMARY KEY,
                match_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                type_id INTEGER NOT NULL,
                player_id INTEGER NOT NULL,
                player_name TEXT NOT NULL,
                location_x REAL NOT NULL,
                location_y REAL NOT NULL,
                end_location_x REAL,
                end_location_y REAL,
                FOREIGN KEY(match_id) REFERENCES match(id)
            )
        """)
        
        db.commit()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        db.close()
        
def insert_event(db, match_id, event):
    cursor = db.cursor()
    cursor.execute("""
        REPLACE INTO match_event (
            id,
            match_id,
            type,
            type_id,
            player_id,
            player_name,
            location_x,
            location_y,
            end_location_x,
            end_location_y
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        event['id'],
        match_id,
        event['type'],
        event['type_id'],
        event['player_id'],
        event['player_name'],
        event['location_x'],
        event['location_y'],
        event['end_location_x'],
        event['end_location_y']
    ))
    db.commit()
    
    return cursor.lastrowid
    
            
def insert_competition(db, competition_id, country_name, competition_name, competition_gender, competition_youth, competition_international):
    cursor = db.cursor()
    cursor.execute("""
        REPLACE INTO competition (
            id,
            country_name,
            competition_name,
            competition_gender,
            competition_youth,
            competition_international
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, (
        competition_id,
        country_name,
        competition_name,
        competition_gender,
        competition_youth,
        competition_international
    ))
    db.commit()
    
    return cursor.lastrowid

def insert_match(db, match_id, season_id):
    cursor = db.cursor()
    cursor.execute("""
        REPLACE INTO match (
            id,
            season_id
        ) VALUES (?, ?)
    """, (
        match_id,
        season_id
    ))
    db.commit()
    
    return cursor.lastrowid

def insert_season(db, competition_id, season_id, season_name):
    cursor = db.cursor()
    cursor.execute("""
        REPLACE INTO season (
            id,
            competition_id,
            name
        ) VALUES (?, ?, ?)
    """, (
        season_id,
        competition_id,
        season_name
    ))
    db.commit()
    
    return cursor.lastrowid

def get_competitions(db):
    cursor = db.cursor()
    cursor.execute("""
        SELECT *
        FROM competition
        ORDER BY id
    """)
    
    competitions = []
    for row in cursor.fetchall():
        competition = {
            'id': row[0],
            'country_name': row[1],
            'competition_name': row[2],
            'competition_gender': row[3],
            'competition_youth': row[4],
            'competition_international': row[5]
        }
        competitions.append(competition)
        
    return competitions
        
def get_matches_in_season(db, season_id):
    cursor = db.cursor()
    cursor.execute("""
        SELECT *
        FROM MATCH
        WHERE season_id = ?
        ORDER BY id
    """, (season_id,))
    
    matches = []
    for row in cursor.fetchall():
        match = {
            'id': row[0],
        }
        matches.append(match)
        
    return matches
          
def get_seasons_for_competition(db, competition_id):
    cursor = db.cursor()
    cursor.execute("""
        SELECT 
            id,
            competition_id,
            name
        FROM season
        WHERE competition_id = ?
        ORDER BY id
    """, (competition_id,))
        
    seasons = []
    for row in cursor.fetchall():
        season = {
            'id': row[0],
            'competition_id': row[1],
            'name': row[2]
        }
        seasons.append(season)
        
    return seasons
    
def drop_all_tables():
    """Drop all tables in the database"""
    logger.warning("Dropping all database tables!")
    db = get_db()
    try:
        # Get all table names
        cursor = db.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%';
        """)
        tables = cursor.fetchall()
        
        # Drop each table
        for table in tables:
            logger.info(f"Dropping table: {table['name']}")
            db.execute(f"DROP TABLE IF EXISTS {table['name']}")
        
        db.commit()
        logger.info("All tables dropped successfully")
    except Exception as e:
        logger.error(f"Error dropping tables: {e}")
        raise
    finally:
        db.close()