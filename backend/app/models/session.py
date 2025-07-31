from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class GameSession(Base):
    __tablename__ = "game_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, nullable=False)
    game_id = Column(Integer, nullable=False)
    parent_id = Column(Integer, nullable=False)
    
    # Session details
    session_id = Column(String, unique=True, nullable=False)  # UUID for session
    difficulty_level = Column(String, default="beginner")
    
    # Timing
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Float, nullable=True)
    
    # Session state
    status = Column(String, default="active")  # active, completed, abandoned, error
    completion_percentage = Column(Float, default=0.0)
    
    # Behavioral data
    interactions = Column(JSON, nullable=True)  # Detailed interaction data
    responses = Column(JSON, nullable=True)  # Game responses and choices
    emotional_reactions = Column(JSON, nullable=True)  # Detected emotions
    attention_metrics = Column(JSON, nullable=True)  # Focus and attention data
    
    # Performance metrics
    score = Column(Float, nullable=True)
    accuracy = Column(Float, nullable=True)
    speed_metrics = Column(JSON, nullable=True)  # Response times, etc.
    
    # Technical data
    device_info = Column(JSON, nullable=True)  # Browser, OS, screen size
    network_conditions = Column(JSON, nullable=True)  # Connection quality
    
    # Error tracking
    errors_encountered = Column(JSON, nullable=True)
    technical_issues = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<GameSession(id={self.id}, child_id={self.child_id}, game_id={self.game_id}, status='{self.status}')>" 