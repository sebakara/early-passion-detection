from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, JSON, Float, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Question details
    question_text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)  # multiple_choice, rating, open_ended, scenario
    category = Column(String, nullable=False)  # art, music, science, sports, leadership, etc.
    talent_domain = Column(String, nullable=False)  # specific talent being tested
    
    # Options for multiple choice questions
    options = Column(JSON, nullable=True)  # Array of options for multiple choice
    
    # Age and difficulty
    min_age = Column(Integer, default=3)
    max_age = Column(Integer, default=12)
    difficulty_level = Column(String, default="easy")  # easy, medium, hard
    
    # Scoring and analysis
    scoring_weights = Column(JSON, nullable=True)  # Weights for different answers
    expected_duration = Column(Integer, default=30)  # Expected time in seconds
    
    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Question(id={self.id}, category='{self.category}', talent_domain='{self.talent_domain}')>"

class QuestionResponse(Base):
    __tablename__ = "question_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=True)
    
    # Response data
    answer = Column(Text, nullable=False)  # The child's answer
    response_time = Column(Float, nullable=True)  # Time taken to answer in seconds
    confidence_level = Column(Float, nullable=True)  # Child's confidence (1-10)
    
    # Analysis results
    score = Column(Float, nullable=True)  # Calculated score for this question
    talent_indicators = Column(JSON, nullable=True)  # Detected talent indicators
    
    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<QuestionResponse(id={self.id}, child_id={self.child_id}, question_id={self.question_id})>"

class TalentAssessment(Base):
    __tablename__ = "talent_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Relationships
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=True)
    
    # Assessment results
    talent_domains = Column(JSON, nullable=False)  # Array of detected talent domains with scores
    primary_talent = Column(String, nullable=True)  # Primary detected talent
    secondary_talents = Column(JSON, nullable=True)  # Secondary talents
    confidence_score = Column(Float, nullable=True)  # Overall confidence in assessment
    
    # Detailed analysis
    behavioral_patterns = Column(JSON, nullable=True)  # Observed behavioral patterns
    response_patterns = Column(JSON, nullable=True)  # Response time and pattern analysis
    interest_indicators = Column(JSON, nullable=True)  # Interest level indicators
    
    # Recommendations
    recommended_activities = Column(JSON, nullable=True)  # Recommended activities
    development_path = Column(JSON, nullable=True)  # Suggested development path
    
    # Metadata
    assessment_date = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<TalentAssessment(id={self.id}, child_id={self.child_id}, primary_talent='{self.primary_talent}')>" 