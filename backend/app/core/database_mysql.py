from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("database_mysql")

def create_db():
    """Initialize database connection and return necessary components."""
    try:
        # Get database configuration from environment variables
        DB_HOST = os.environ.get("DB_HOST")
        DB_PORT = os.environ.get("DB_PORT")
        DB_USER = os.environ.get("DB_USER")
        DB_PASSWORD = os.environ.get("DB_PASSWORD")
        DB_NAME = os.environ.get("DB_NAME")
        database_url = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
        logger.info(f"Connecting to MySQL database at {DB_HOST}:{DB_PORT}/{DB_NAME}...")
        
        engine = create_engine(database_url)
        logger.info("MySQL database connection established successfully!")
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        
        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
        
        return {
            'engine': engine,
            'SessionLocal': SessionLocal,
            'Base': Base,
            'get_db': get_db
        }
    except Exception as e:
        logger.error(f"Failed to connect to MySQL database: {e}")
        raise