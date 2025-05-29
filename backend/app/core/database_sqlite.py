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

def create_db():
    """Initialize database connection and return necessary components."""
    try:
        logger.info("Creating in-memory SQLite database...")
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        logger.info("In-memory SQLite database created successfully!")
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()
        
        def get_db():
            db = SessionLocal()
            try:
                # Ensure tables are created for this session
                Base.metadata.create_all(bind=engine)
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
        logger.error(f"Failed to create SQLite database: {e}")
        raise
