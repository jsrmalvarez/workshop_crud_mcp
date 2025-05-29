from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import logging
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get database configuration from environment variables
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("database")

# Configure retry settings
MAX_RETRIES = 60  # Maximum number of connection attempts
RETRY_INTERVAL = 2  # Seconds to wait between retries

# Try to establish a connection with retries
def get_engine():
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Attempting to connect to database (attempt {attempt + 1}/{MAX_RETRIES})...")
            engine = create_engine(DATABASE_URL)
            # Test connection
            connection = engine.connect()
            connection.close()
            logger.info("Database connection established successfully!")
            return engine
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying in {RETRY_INTERVAL} seconds...")
                time.sleep(RETRY_INTERVAL)
            else:
                logger.error("Max retries reached. Unable to connect to database.")
                raise
    # If we get here, we've exhausted all retries
    raise Exception("Failed to connect to database after maximum retry attempts")

# Initialize connection outside of the function to ensure it happens at startup
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()