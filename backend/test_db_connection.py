#!/usr/bin/env python3
"""
Simple Database Connection Test Script
Quick test to verify database connectivity and basic operations.
"""

import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.core.database import engine, SessionLocal
from sqlalchemy import text

def test_connection():
    """Test basic database connection"""
    print("Testing database connection...")
    print(f"Database URL: {settings.DATABASE_URL}")
    
    try:
        # Test connection using SQLAlchemy engine
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()
            print(f"✅ Database connection successful!")
            print(f"   PostgreSQL version: {version[0]}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_session():
    """Test database session creation"""
    print("\nTesting database session...")
    
    try:
        db = SessionLocal()
        result = db.execute(text("SELECT 1 as test;"))
        test_value = result.fetchone()
        db.close()
        
        if test_value and test_value[0] == 1:
            print("✅ Database session test successful!")
            return True
        else:
            print("❌ Database session test failed!")
            return False
    except Exception as e:
        print(f"❌ Database session test failed: {e}")
        return False

def test_tables():
    """Test if tables exist"""
    print("\nTesting table existence...")
    
    try:
        with engine.connect() as connection:
            # Check for users table
            result = connection.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'users'
                );
            """))
            users_exists = result.fetchone()[0]
            
            # Check for children table
            result = connection.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'children'
                );
            """))
            children_exists = result.fetchone()[0]
            
            # Check for games table
            result = connection.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'games'
                );
            """))
            games_exists = result.fetchone()[0]
            
            print(f"   Users table: {'✅' if users_exists else '❌'}")
            print(f"   Children table: {'✅' if children_exists else '❌'}")
            print(f"   Games table: {'✅' if games_exists else '❌'}")
            
            return users_exists and children_exists and games_exists
            
    except Exception as e:
        print(f"❌ Table test failed: {e}")
        return False

def main():
    """Run all database tests"""
    print("=" * 50)
    print("Database Connection Test")
    print("=" * 50)
    
    # Test 1: Basic connection
    connection_ok = test_connection()
    
    # Test 2: Session creation
    session_ok = test_session()
    
    # Test 3: Table existence
    tables_ok = test_tables()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print(f"   Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"   Session: {'✅ PASS' if session_ok else '❌ FAIL'}")
    print(f"   Tables: {'✅ PASS' if tables_ok else '❌ FAIL'}")
    
    if connection_ok and session_ok and tables_ok:
        print("\n🎉 All tests passed! Database is ready to use.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check your database configuration.")
        sys.exit(1)

if __name__ == "__main__":
    main() 