from typing import Dict, Any
from app.core import database_sqlite, database_mysql
import os
def init_sqlite() -> Dict[str, Any]:
    """Initialize SQLite database"""    
    return database_sqlite.create_db()

def init_mysql() -> Dict[str, Any]:
    """Initialize MySQL database with given credentials"""
    
    return database_mysql.create_db()

if os.environ.get("DB_TYPE") == "mysql":
    # Initialize MySQL database
    db_components = init_mysql()
else:
    # Initialize SQLite database        
    db_components = init_sqlite()
    
# Export components
engine = db_components['engine']
SessionLocal = db_components['SessionLocal']
Base = db_components['Base']
get_db = db_components['get_db']