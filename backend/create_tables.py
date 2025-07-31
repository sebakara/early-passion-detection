#!/usr/bin/env python3
"""
Simple script to create database tables
"""

import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.database import Base, engine
from app.models.user import User
from app.models.child import Child
from app.models.game import Game
from app.models.session import GameSession
from app.models.passion import PassionDomain, PassionInsight

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
        from app.core.database import SessionLocal
        from passlib.context import CryptContext
        
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        def get_password_hash(password: str) -> str:
            return pwd_context.hash(password)
        
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
            is_admin=True,
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
        from app.core.database import SessionLocal
        
        db = SessionLocal()
        
        # Check if games already exist
        existing_games = db.query(Game).count()
        if existing_games > 0:
            print("✅ Sample games already exist")
            db.close()
            return True
        
        # Sample games data
        sample_games = [
            Game(
                name="Color Matching Adventure",
                description="Match colors and shapes in a fun adventure game",
                category="puzzle",
                config={"type": "matching", "difficulty": "easy"},
                age_range={"min": 3, "max": 6},
                estimated_duration=10,
                passion_domains=["art_creativity", "logic_mathematics"],
                is_active=True
            ),
            Game(
                name="Musical Rhythm Maker",
                description="Create rhythms and learn about music",
                category="music",
                config={"type": "rhythm", "difficulty": "medium"},
                age_range={"min": 4, "max": 8},
                estimated_duration=15,
                passion_domains=["music_rhythm"],
                is_active=True
            ),
            Game(
                name="Science Explorer",
                description="Discover the wonders of science through experiments",
                category="science",
                config={"type": "experiment", "difficulty": "medium"},
                age_range={"min": 5, "max": 10},
                estimated_duration=20,
                passion_domains=["science_discovery"],
                is_active=True
            ),
            Game(
                name="Sports Challenge",
                description="Fun physical activities and sports games",
                category="sports",
                config={"type": "physical", "difficulty": "easy"},
                age_range={"min": 4, "max": 9},
                estimated_duration=12,
                passion_domains=["sports_movement"],
                is_active=True
            ),
            Game(
                name="Story Creator",
                description="Create and share imaginative stories",
                category="language",
                config={"type": "creative", "difficulty": "medium"},
                age_range={"min": 6, "max": 12},
                estimated_duration=18,
                passion_domains=["language_communication", "art_creativity"],
                is_active=True
            )
        ]
        
        for game in sample_games:
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
    """Main function"""
    print("=" * 60)
    print("Passion Detection AI - Table Creation")
    print("=" * 60)
    
    # Step 1: Create tables
    if not create_tables():
        sys.exit(1)
    
    # Step 2: Create admin user
    if not create_admin_user():
        sys.exit(1)
    
    # Step 3: Seed sample games
    if not seed_sample_games():
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 Database setup completed successfully!")
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