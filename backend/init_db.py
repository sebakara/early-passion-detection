#!/usr/bin/env python3
"""
Database Initialization Script
This script initializes the database for the Passion Detection AI application.
It can be used both for local development and Docker deployment.
"""

import os
import sys
import time
from pathlib import Path

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
from app.core.auth import get_password_hash

def wait_for_database(max_retries=30, delay=2):
    """Wait for database to be available"""
    print("Waiting for database to be available...")
    
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                connection.execute("SELECT 1")
                print("✅ Database is available!")
                return True
        except Exception as e:
            print(f"Attempt {attempt + 1}/{max_retries}: Database not ready yet...")
            if attempt < max_retries - 1:
                time.sleep(delay)
    
    print("❌ Database connection failed after maximum retries")
    return False

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def create_admin_user():
    """Create a default admin user"""
    print("Creating admin user...")
    
    try:
        db = SessionLocal()
        
        # Check if admin user already exists
        admin_user = db.query(User).filter(User.email == "admin@passiondetection.com").first()
        
        if admin_user:
            print("✅ Admin user already exists")
            db.close()
            return True
        
        # Create admin user
        admin_user = User(
            email="admin@passiondetection.com",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        db.close()
        
        print("✅ Admin user created successfully!")
        print("   Email: admin@passiondetection.com")
        print("   Password: admin123")
        return True
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.close()
        return False

def seed_sample_games():
    """Seed sample games for testing"""
    print("Seeding sample games...")
    
    try:
        db = SessionLocal()
        
        # Check if games already exist
        existing_games = db.query(Game).count()
        if existing_games > 0:
            print("✅ Sample games already exist")
            db.close()
            return True
        
        # Sample games data
        sample_games = [
            {
                "name": "Color Matching Adventure",
                "description": "Match colors and shapes in a fun adventure game",
                "category": "puzzle",
                "age_min": 3,
                "age_max": 6,
                "duration_minutes": 10,
                "passion_domains": ["art_creativity", "logic_mathematics"],
                "difficulty_level": "easy",
                "is_active": True
            },
            {
                "name": "Musical Rhythm Maker",
                "description": "Create rhythms and learn about music",
                "category": "music",
                "age_min": 4,
                "age_max": 8,
                "duration_minutes": 15,
                "passion_domains": ["music_rhythm"],
                "difficulty_level": "medium",
                "is_active": True
            },
            {
                "name": "Science Explorer",
                "description": "Discover the wonders of science through experiments",
                "category": "science",
                "age_min": 5,
                "age_max": 10,
                "duration_minutes": 20,
                "passion_domains": ["science_discovery"],
                "difficulty_level": "medium",
                "is_active": True
            },
            {
                "name": "Sports Challenge",
                "description": "Fun physical activities and sports games",
                "category": "sports",
                "age_min": 4,
                "age_max": 9,
                "duration_minutes": 12,
                "passion_domains": ["sports_movement"],
                "difficulty_level": "easy",
                "is_active": True
            },
            {
                "name": "Story Creator",
                "description": "Create and share imaginative stories",
                "category": "language",
                "age_min": 6,
                "age_max": 12,
                "duration_minutes": 18,
                "passion_domains": ["language_communication", "art_creativity"],
                "difficulty_level": "medium",
                "is_active": True
            },
            {
                "name": "Math Adventure",
                "description": "Learn mathematics through interactive games",
                "category": "education",
                "age_min": 5,
                "age_max": 10,
                "duration_minutes": 15,
                "passion_domains": ["logic_mathematics"],
                "difficulty_level": "medium",
                "is_active": True
            },
            {
                "name": "Leadership Quest",
                "description": "Develop leadership skills through team activities",
                "category": "social",
                "age_min": 7,
                "age_max": 12,
                "duration_minutes": 25,
                "passion_domains": ["leadership_social"],
                "difficulty_level": "hard",
                "is_active": True
            }
        ]
        
        # Create game objects
        for game_data in sample_games:
            game = Game(**game_data)
            db.add(game)
        
        db.commit()
        db.close()
        
        print(f"✅ {len(sample_games)} sample games created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error seeding sample games: {e}")
        db.close()
        return False

def main():
    """Main initialization function"""
    print("=" * 60)
    print("Passion Detection AI - Database Initialization")
    print("=" * 60)
    
    # Step 1: Wait for database
    if not wait_for_database():
        sys.exit(1)
    
    # Step 2: Create tables
    if not create_tables():
        sys.exit(1)
    
    # Step 3: Create admin user
    if not create_admin_user():
        sys.exit(1)
    
    # Step 4: Seed sample games
    if not seed_sample_games():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Database initialization completed successfully!")
    print("=" * 60)
    print("\nYou can now:")
    print("1. Start the FastAPI server: uvicorn main:app --reload")
    print("2. Access the API documentation: http://localhost:8000/docs")
    print("3. Login with admin credentials:")
    print("   Email: admin@passiondetection.com")
    print("   Password: admin123")
    print("\nHappy coding! 🚀")

if __name__ == "__main__":
    main() 