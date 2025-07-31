#!/usr/bin/env python3
"""
Database Setup Script for Passion Detection AI
This script handles database creation, connection testing, and initial setup.
"""

import os
import sys
import logging
from pathlib import Path
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.core.database import Base, engine, SessionLocal
from app.models.user import User
from app.models.child import Child
from app.models.game import Game
from app.models.session import GameSession
from app.models.passion import PassionDomain, PassionInsight

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DatabaseSetup:
    def __init__(self):
        self.database_url = settings.DATABASE_URL
        self.db_name = self._extract_db_name()
        self.db_user = self._extract_db_user()
        self.db_password = self._extract_db_password()
        self.db_host = self._extract_db_host()
        self.db_port = self._extract_db_port()
        
    def _extract_db_name(self):
        """Extract database name from DATABASE_URL"""
        try:
            return self.database_url.split('/')[-1]
        except:
            return "passion_detection"
    
    def _extract_db_user(self):
        """Extract database user from DATABASE_URL"""
        try:
            return self.database_url.split('://')[1].split(':')[0]
        except:
            return "user"
    
    def _extract_db_password(self):
        """Extract database password from DATABASE_URL"""
        try:
            return self.database_url.split(':')[2].split('@')[0]
        except:
            return "password"
    
    def _extract_db_host(self):
        """Extract database host from DATABASE_URL"""
        try:
            return self.database_url.split('@')[1].split(':')[0]
        except:
            return "localhost"
    
    def _extract_db_port(self):
        """Extract database port from DATABASE_URL"""
        try:
            return int(self.database_url.split(':')[-1].split('/')[0])
        except:
            return 5432
    
    def create_database(self):
        """Create the database if it doesn't exist"""
        try:
            # Connect to PostgreSQL server (not to a specific database)
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database="kidedutech" 
            )
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            
            # Check if database exists
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (self.db_name,))
            exists = cursor.fetchone()
            
            if not exists:
                logger.info(f"Creating database '{self.db_name}'...")
                cursor.execute(f'CREATE DATABASE "{self.db_name}"')
                logger.info(f"Database '{self.db_name}' created successfully!")
            else:
                logger.info(f"Database '{self.db_name}' already exists.")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            logger.error(f"Error creating database: {e}")
            return False
    
    def test_connection(self):
        """Test database connection"""
        try:
            # Test connection to the specific database
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                password=self.db_password,
                database=self.db_name
            )
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            logger.info(f"Database connection successful! PostgreSQL version: {version[0]}")
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def create_tables(self):
        """Create all database tables"""
        try:
            logger.info("Creating database tables...")
            Base.metadata.create_all(bind=engine)
            logger.info("All tables created successfully!")
            return True
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
            return False
    
    def verify_tables(self):
        """Verify that all tables were created"""
        try:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            expected_tables = [
                'users', 'children', 'games', 'game_sessions', 
                'passion_domains', 'passion_insights'
            ]
            
            missing_tables = [table for table in expected_tables if table not in tables]
            
            if missing_tables:
                logger.warning(f"Missing tables: {missing_tables}")
                return False
            else:
                logger.info("All expected tables are present!")
                return True
        except Exception as e:
            logger.error(f"Error verifying tables: {e}")
            return False
    
    def seed_initial_data(self):
        """Seed initial data for development"""
        try:
            db = SessionLocal()
            
            # Check if data already exists
            existing_users = db.query(User).count()
            if existing_users > 0:
                logger.info("Database already contains data, skipping seeding.")
                db.close()
                return True
            
            logger.info("Seeding initial data...")
            
            # Create sample games
            sample_games = [
                Game(
                    name="Color Matching Adventure",
                    description="Match colors and shapes in a fun adventure game",
                    category="puzzle",
                    age_min=3,
                    age_max=6,
                    duration_minutes=10,
                    passion_domains=["art_creativity", "logic_mathematics"],
                    difficulty_level="easy",
                    is_active=True
                ),
                Game(
                    name="Musical Rhythm Maker",
                    description="Create rhythms and learn about music",
                    category="music",
                    age_min=4,
                    age_max=8,
                    duration_minutes=15,
                    passion_domains=["music_rhythm"],
                    difficulty_level="medium",
                    is_active=True
                ),
                Game(
                    name="Science Explorer",
                    description="Discover the wonders of science through experiments",
                    category="science",
                    age_min=5,
                    age_max=10,
                    duration_minutes=20,
                    passion_domains=["science_discovery"],
                    difficulty_level="medium",
                    is_active=True
                ),
                Game(
                    name="Sports Challenge",
                    description="Fun physical activities and sports games",
                    category="sports",
                    age_min=4,
                    age_max=9,
                    duration_minutes=12,
                    passion_domains=["sports_movement"],
                    difficulty_level="easy",
                    is_active=True
                ),
                Game(
                    name="Story Creator",
                    description="Create and share imaginative stories",
                    category="language",
                    age_min=6,
                    age_max=12,
                    duration_minutes=18,
                    passion_domains=["language_communication", "art_creativity"],
                    difficulty_level="medium",
                    is_active=True
                )
            ]
            
            for game in sample_games:
                db.add(game)
            
            db.commit()
            logger.info(f"Seeded {len(sample_games)} sample games")
            
            db.close()
            return True
            
        except Exception as e:
            logger.error(f"Error seeding data: {e}")
            db.close()
            return False
    
    def run_setup(self, seed_data=False):
        """Run the complete database setup process"""
        logger.info("Starting database setup...")
        
        # Step 1: Create database
        if not self.create_database():
            logger.error("Failed to create database. Exiting.")
            return False
        
        # Step 2: Test connection
        if not self.test_connection():
            logger.error("Failed to connect to database. Exiting.")
            return False
        
        # Step 3: Create tables
        if not self.create_tables():
            logger.error("Failed to create tables. Exiting.")
            return False
        
        # Step 4: Verify tables
        if not self.verify_tables():
            logger.error("Table verification failed. Exiting.")
            return False
        
        # Step 5: Seed data (optional)
        if seed_data:
            if not self.seed_initial_data():
                logger.warning("Failed to seed initial data, but setup completed.")
        
        logger.info("Database setup completed successfully!")
        return True

def main():
    """Main function to run database setup"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Database setup for Passion Detection AI")
    parser.add_argument(
        "--seed", 
        action="store_true", 
        help="Seed initial data for development"
    )
    parser.add_argument(
        "--test-only", 
        action="store_true", 
        help="Only test database connection"
    )
    
    args = parser.parse_args()
    
    setup = DatabaseSetup()
    
    if args.test_only:
        if setup.test_connection():
            logger.info("Database connection test passed!")
            sys.exit(0)
        else:
            logger.error("Database connection test failed!")
            sys.exit(1)
    
    success = setup.run_setup(seed_data=args.seed)
    
    if success:
        logger.info("Setup completed successfully!")
        sys.exit(0)
    else:
        logger.error("Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 