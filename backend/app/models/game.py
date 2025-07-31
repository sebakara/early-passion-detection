from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)  # art, music, science, sports, leadership, language, logic
    
    # Game configuration
    config = Column(JSON, nullable=False)  # Game-specific configuration
    difficulty_levels = Column(JSON, nullable=True)  # Available difficulty levels
    age_range = Column(JSON, nullable=False)  # {"min": 3, "max": 8}
    
    # Game mechanics
    estimated_duration = Column(Integer, nullable=True)  # in minutes
    max_players = Column(Integer, default=1)
    requires_audio = Column(Boolean, default=False)
    requires_video = Column(Boolean, default=False)
    requires_microphone = Column(Boolean, default=False)
    
    # Passion domains this game can detect
    passion_domains = Column(JSON, nullable=False)  # List of domains this game targets
    
    # Game state
    is_active = Column(Boolean, default=True)
    is_beta = Column(Boolean, default=False)
    version = Column(String, default="1.0.0")
    
    # Analytics
    total_plays = Column(Integer, default=0)
    average_rating = Column(Float, default=0.0)
    average_completion_time = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Game(id={self.id}, name='{self.name}', category='{self.category}')>" 