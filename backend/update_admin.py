#!/usr/bin/env python3
"""
Update admin user to be a parent
"""

from app.core.database import SessionLocal
from app.models.user import User

def update_admin_user():
    """Update admin user to be a parent"""
    print("Updating admin user...")
    
    try:
        db = SessionLocal()
        
        # Find admin user
        admin_user = db.query(User).filter(User.email == "admin@passiondetection.com").first()
        
        if admin_user:
            # Update to be a parent
            admin_user.is_parent = True
            db.commit()
            print("✅ Admin user updated successfully!")
            print(f"   Email: {admin_user.email}")
            print(f"   Is Parent: {admin_user.is_parent}")
            print(f"   Is Admin: {admin_user.is_admin}")
        else:
            print("❌ Admin user not found")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Error updating admin user: {e}")
        db.close()

if __name__ == "__main__":
    update_admin_user() 