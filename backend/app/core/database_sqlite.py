from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("database_sqlite")

# SQLite URL for in-memory database
DATABASE_URL = "sqlite:///:memory:"

def get_engine():
    try:
        logger.info("Creating in-memory SQLite database...")
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        logger.info("In-memory SQLite database created successfully!")
        return engine
    except Exception as e:
        logger.error(f"Failed to create SQLite database: {e}")
        raise

# Initialize connection
engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        # Ensure tables are created for this session
        Base.metadata.create_all(bind=engine)
        yield db
    finally:
        db.close()
