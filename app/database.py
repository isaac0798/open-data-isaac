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
                id INTEGER PRIMARY KEY,
                match_id INTEGER,
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