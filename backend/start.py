import time
import os
import logging
import subprocess
import pymysql

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("startup")

# Database connection parameters
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = int(os.environ.get("DB_PORT"))
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

MAX_RETRIES = 60
RETRY_INTERVAL = 2

def wait_for_database():
    """Wait for the database to become available."""
    logger.info(f"Waiting for database at {DB_HOST}:{DB_PORT}...")
    
    for attempt in range(MAX_RETRIES):
        try:
            connection = pymysql.connect(
                host=DB_HOST,
                port=DB_PORT,
                user=DB_USER,
                password=DB_PASSWORD,
            )
            connection.close()
            logger.info("Database connection established successfully!")
            return True
        except Exception as e:
            logger.warning(f"Database connection attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                logger.info(f"Retrying in {RETRY_INTERVAL} seconds...")
                time.sleep(RETRY_INTERVAL)
            else:
                logger.error("Maximum number of retries reached. Giving up.")
                return False
    return False

if __name__ == "__main__":
    # Wait for database to be ready
    if wait_for_database():
        logger.info("Starting FastAPI application...")
        # Start the FastAPI application using uvicorn
        subprocess.run(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    else:
        logger.error("Failed to connect to the database. Exiting.")
        exit(1)