from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    is_parent = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Parent-specific fields
    phone_number = Column(String, nullable=True)
    address = Column(Text, nullable=True)
    
    # Child-specific fields (if user is a child)
    date_of_birth = Column(DateTime, nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    parent_id = Column(Integer, nullable=True)  # Reference to parent user
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', is_parent={self.is_parent})>" 