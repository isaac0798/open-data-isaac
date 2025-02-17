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
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            )
        """)
        
        # Add any other tables you need here
        
        db.commit()
        logger.info("Database initialization completed successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise
    finally:
        db.close()