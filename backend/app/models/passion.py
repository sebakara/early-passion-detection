from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float
from sqlalchemy.sql import func
from app.core.database import Base
from datetime import datetime

class PassionDomain(Base):
    __tablename__ = "passion_domains"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, nullable=False)
    
    # Domain information
    domain = Column(String, nullable=False)  # art, music, science, sports, leadership, language, logic
    confidence_score = Column(Float, nullable=False)  # 0.0 to 1.0
    strength_level = Column(String, nullable=False)  # low, medium, high, very_high
    
    # Detection details
    detection_method = Column(String, nullable=False)  # rule_based, ml_model, hybrid
    model_version = Column(String, nullable=True)
    data_points_used = Column(Integer, default=0)
    
    # Evidence and reasoning
    supporting_evidence = Column(JSON, nullable=True)  # Specific behaviors that support this domain
    games_played = Column(JSON, nullable=True)  # List of games that contributed to this detection
    behavioral_patterns = Column(JSON, nullable=True)  # Key behavioral indicators
    
    # Development tracking
    first_detected = Column(DateTime(timezone=True), server_default=func.now())
    last_updated = Column(DateTime(timezone=True), onupdate=func.now())
    trend = Column(String, nullable=True)  # increasing, decreasing, stable
    
    # Recommendations
    recommended_activities = Column(JSON, nullable=True)
    difficulty_progression = Column(JSON, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)  # Verified by parent or expert
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<PassionDomain(id={self.id}, child_id={self.child_id}, domain='{self.domain}', confidence={self.confidence_score})>"

class PassionInsight(Base):
    __tablename__ = "passion_insights"
    
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, nullable=False)
    
    # Insight details
    insight_type = Column(String, nullable=False)  # pattern, trend, recommendation, milestone
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    
    # Data
    data = Column(JSON, nullable=True)  # Supporting data for the insight
    related_domains = Column(JSON, nullable=True)  # Related passion domains
    
    # Importance and visibility
    importance_score = Column(Float, default=0.5)  # 0.0 to 1.0
    is_highlighted = Column(Boolean, default=False)
    
    # Parent notification
    notify_parent = Column(Boolean, default=False)
    parent_notified = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<PassionInsight(id={self.id}, child_id={self.child_id}, type='{self.insight_type}', title='{self.title}')>" 