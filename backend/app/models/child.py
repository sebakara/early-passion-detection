from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Child(Base):
    __tablename__ = "children"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)  # Reference to User table
    parent_id = Column(Integer, nullable=False)  # Reference to parent User
    
    # Basic information
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    date_of_birth = Column(DateTime, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=True)
    
    # Preferences and interests (stored as JSON)
    initial_interests = Column(JSON, nullable=True)  # Initial parent-reported interests
    favorite_colors = Column(JSON, nullable=True)
    favorite_activities = Column(JSON, nullable=True)
    learning_style = Column(String, nullable=True)  # visual, auditory, kinesthetic
    
    # Development tracking
    current_level = Column(String, default="beginner")  # beginner, intermediate, advanced
    total_play_time = Column(Float, default=0.0)  # Total time spent in minutes
    sessions_completed = Column(Integer, default=0)
    
    # Privacy and consent
    parental_consent_given = Column(Boolean, default=False)
    consent_date = Column(DateTime, nullable=True)
    data_sharing_preferences = Column(JSON, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_activity = Column(DateTime(timezone=True), nullable=True)
    
    def __repr__(self):
        return f"<Child(id={self.id}, name='{self.first_name}', age={self.age})>" 