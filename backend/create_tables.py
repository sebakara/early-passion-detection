#!/usr/bin/env python3
"""
Create database tables and seed initial data
"""

import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.database import engine, SessionLocal
from app.models.user import User
from app.models.child import Child
from app.models.game import Game
from app.models.question import Question, QuestionResponse, TalentAssessment
from app.models.session import GameSession
from app.models.passion import PassionDomain, PassionInsight
from passlib.context import CryptContext

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    
    try:
        # Import all models to ensure they're registered
        from app.models.user import Base
        from app.models.child import Base
        from app.models.game import Base
        from app.models.question import Base
        from app.models.session import Base
        from app.models.passion import Base
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def create_admin_user():
    """Create admin user"""
    print("Creating admin user...")
    
    try:
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
            is_parent=True,
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
            ),
            Game(
                name="Team Builder",
                description="Work together with friends to solve challenges",
                category="social",
                config={"type": "collaborative", "difficulty": "medium"},
                age_range={"min": 5, "max": 10},
                estimated_duration=15,
                passion_domains=["leadership_social"],
                is_active=True
            ),
            Game(
                name="Math Adventure",
                description="Learn math through fun interactive games",
                category="education",
                config={"type": "learning", "difficulty": "easy"},
                age_range={"min": 4, "max": 8},
                estimated_duration=12,
                passion_domains=["logic_mathematics"],
                is_active=True
            ),
            Game(
                name="Tech Explorer",
                description="Learn about technology and coding basics",
                category="technology",
                config={"type": "learning", "difficulty": "hard"},
                age_range={"min": 7, "max": 12},
                estimated_duration=25,
                passion_domains=["technology_innovation"],
                is_active=True
            )
        ]
        
        for game in sample_games:
            db.add(game)
        
        db.commit()
        db.close()
        
        print(f"✅ Added {len(sample_games)} sample games")
        return True
        
    except Exception as e:
        print(f"❌ Error seeding games: {e}")
        db.close()
        return False

def seed_sample_questions():
    """Seed sample questions for talent detection"""
    print("Seeding sample questions...")
    
    try:
        from app.core.database import SessionLocal
        
        db = SessionLocal()
        
        # Check if questions already exist
        existing_questions = db.query(Question).count()
        if existing_questions > 0:
            print("✅ Sample questions already exist")
            db.close()
            return True
        
        # Import the seed_questions function
        from seed_questions import seed_questions
        return seed_questions()
        
    except Exception as e:
        print(f"❌ Error seeding questions: {e}")
        return False

def main():
    """Main function to set up the database"""
    print("=" * 60)
    print("Passion Detection AI - Table Creation")
    print("=" * 60)
    
    # Create tables
    if not create_tables():
        return False
    
    # Create admin user
    if not create_admin_user():
        return False
    
    # Seed sample games
    if not seed_sample_games():
        return False
    
    # Seed sample questions
    if not seed_sample_questions():
        return False
    
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
    return True

if __name__ == "__main__":
    main() 