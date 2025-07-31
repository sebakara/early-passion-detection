"""
Database Utilities
Helper functions for database operations and connection management.
"""

import logging
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError, ProgrammingError
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from app.core.config import settings
from app.core.database import engine, SessionLocal

logger = logging.getLogger(__name__)

def get_database_info() -> Dict[str, Any]:
    """Get database connection information"""
    return {
        "host": settings.DATABASE_URL.split('@')[1].split(':')[0] if '@' in settings.DATABASE_URL else "localhost",
        "port": int(settings.DATABASE_URL.split(':')[-1].split('/')[0]) if ':' in settings.DATABASE_URL else 5432,
        "database": settings.DATABASE_URL.split('/')[-1],
        "user": settings.DATABASE_URL.split('://')[1].split(':')[0] if '://' in settings.DATABASE_URL else "user"
    }

def test_connection() -> bool:
    """Test database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            result.fetchone()
            return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False

def get_database_stats() -> Dict[str, Any]:
    """Get database statistics"""
    try:
        db = SessionLocal()
        
        # Get table counts
        tables = ['users', 'children', 'games', 'game_sessions', 'passion_domains', 'passion_insights']
        stats = {}
        
        for table in tables:
            try:
                result = db.execute(text(f"SELECT COUNT(*) FROM {table}"))
                count = result.fetchone()[0]
                stats[f"{table}_count"] = count
            except Exception as e:
                logger.warning(f"Could not get count for table {table}: {e}")
                stats[f"{table}_count"] = 0
        
        db.close()
        return stats
        
    except Exception as e:
        logger.error(f"Error getting database stats: {e}")
        return {}

def create_database_if_not_exists() -> bool:
    """Create database if it doesn't exist"""
    try:
        db_info = get_database_info()
        
        # Connect to PostgreSQL server (not to a specific database)
        conn = psycopg2.connect(
            host=db_info["host"],
            port=db_info["port"],
            user=db_info["user"],
            password=settings.DATABASE_URL.split(':')[2].split('@')[0] if ':' in settings.DATABASE_URL else "password",
            database="postgres"  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_info["database"],))
        exists = cursor.fetchone()
        
        if not exists:
            logger.info(f"Creating database '{db_info['database']}'...")
            cursor.execute(f'CREATE DATABASE "{db_info["database"]}"')
            logger.info(f"Database '{db_info['database']}' created successfully!")
        else:
            logger.info(f"Database '{db_info['database']}' already exists.")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        return False

def wait_for_database(max_retries: int = 30, delay: int = 2) -> bool:
    """Wait for database to be available"""
    logger.info("Waiting for database to be available...")
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                logger.info("Database is available!")
                return True
        except Exception as e:
            logger.info(f"Attempt {attempt + 1}/{max_retries}: Database not ready yet...")
            if attempt < max_retries - 1:
                import time
                time.sleep(delay)
    
    logger.error("Database connection failed after maximum retries")
    return False

def get_table_info(table_name: str) -> Optional[Dict[str, Any]]:
    """Get information about a specific table"""
    try:
        db = SessionLocal()
        
        # Get table structure
        result = db.execute(text(f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position;
        """))
        
        columns = []
        for row in result.fetchall():
            columns.append({
                "name": row[0],
                "type": row[1],
                "nullable": row[2] == "YES",
                "default": row[3]
            })
        
        # Get row count
        result = db.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        row_count = result.fetchone()[0]
        
        db.close()
        
        return {
            "table_name": table_name,
            "columns": columns,
            "row_count": row_count
        }
        
    except Exception as e:
        logger.error(f"Error getting table info for {table_name}: {e}")
        return None

def backup_database(backup_path: str) -> bool:
    """Create a database backup"""
    try:
        db_info = get_database_info()
        
        import subprocess
        import os
        
        # Create backup directory if it doesn't exist
        os.makedirs(os.path.dirname(backup_path), exist_ok=True)
        
        # Build pg_dump command
        cmd = [
            "pg_dump",
            "-h", db_info["host"],
            "-p", str(db_info["port"]),
            "-U", db_info["user"],
            "-d", db_info["database"],
            "-f", backup_path,
            "--no-password"  # Use environment variable for password
        ]
        
        # Set password environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = settings.DATABASE_URL.split(':')[2].split('@')[0] if ':' in settings.DATABASE_URL else "password"
        
        # Execute backup
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"Database backup created successfully: {backup_path}")
            return True
        else:
            logger.error(f"Database backup failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Error creating database backup: {e}")
        return False

def restore_database(backup_path: str) -> bool:
    """Restore database from backup"""
    try:
        db_info = get_database_info()
        
        import subprocess
        import os
        
        # Build psql command
        cmd = [
            "psql",
            "-h", db_info["host"],
            "-p", str(db_info["port"]),
            "-U", db_info["user"],
            "-d", db_info["database"],
            "-f", backup_path,
            "--no-password"  # Use environment variable for password
        ]
        
        # Set password environment variable
        env = os.environ.copy()
        env["PGPASSWORD"] = settings.DATABASE_URL.split(':')[2].split('@')[0] if ':' in settings.DATABASE_URL else "password"
        
        # Execute restore
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"Database restored successfully from: {backup_path}")
            return True
        else:
            logger.error(f"Database restore failed: {result.stderr}")
            return False
            
    except Exception as e:
        logger.error(f"Error restoring database: {e}")
        return False 