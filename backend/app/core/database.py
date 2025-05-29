import os
from dotenv import load_dotenv
from app.core import database_mysql, database_sqlite

# Load environment variables from .env file
load_dotenv()

# Get database type from environment variable, default to sqlite
DB_TYPE = os.environ.get("DB_TYPE", "mysql").lower()

if DB_TYPE == "mysql":
    # Use MySQL database
    engine = database_mysql.engine
    SessionLocal = database_mysql.SessionLocal
    Base = database_mysql.Base
    get_db = database_mysql.get_db
else:
    # Use SQLite database (default)
    engine = database_sqlite.engine
    SessionLocal = database_sqlite.SessionLocal
    Base = database_sqlite.Base
    get_db = database_sqlite.get_db