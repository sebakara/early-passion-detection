from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class QuestionBase(BaseModel):
    question_text: str
    question_type: str
    category: str
    talent_domain: str
    options: Optional[List[str]] = None
    min_age: int = 3
    max_age: int = 12
    difficulty_level: str = "easy"
    scoring_weights: Optional[Dict[str, float]] = None
    expected_duration: int = 30
    is_active: bool = True

class QuestionCreate(QuestionBase):
    pass

class QuestionUpdate(BaseModel):
    question_text: Optional[str] = None
    question_type: Optional[str] = None
    category: Optional[str] = None
    talent_domain: Optional[str] = None
    options: Optional[List[str]] = None
    min_age: Optional[int] = None
    max_age: Optional[int] = None
    difficulty_level: Optional[str] = None
    scoring_weights: Optional[Dict[str, float]] = None
    expected_duration: Optional[int] = None
    is_active: Optional[bool] = None

class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class QuestionResponseBase(BaseModel):
    child_id: int
    question_id: int
    session_id: Optional[int] = None
    answer: str
    response_time: Optional[float] = None
    confidence_level: Optional[float] = None
    score: Optional[float] = None
    talent_indicators: Optional[Dict[str, Any]] = None

class QuestionResponseCreate(QuestionResponseBase):
    pass

class QuestionResponse(QuestionResponseBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class TalentAssessmentBase(BaseModel):
    child_id: int
    session_id: Optional[int] = None
    talent_domains: Dict[str, float]
    primary_talent: Optional[str] = None
    secondary_talents: Optional[List[str]] = None
    confidence_score: Optional[float] = None
    behavioral_patterns: Optional[Dict[str, Any]] = None
    response_patterns: Optional[Dict[str, Any]] = None
    interest_indicators: Optional[Dict[str, Any]] = None
    recommended_activities: Optional[List[str]] = None
    development_path: Optional[Dict[str, Any]] = None

class TalentAssessmentCreate(TalentAssessmentBase):
    pass

class TalentAssessment(TalentAssessmentBase):
    id: int
    assessment_date: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class QuestionSet(BaseModel):
    """A set of questions for a specific assessment"""
    id: int
    name: str
    description: str
    category: str
    questions: List[Question]
    estimated_duration: int  # in minutes
    target_age_range: Dict[str, int]
    
    class Config:
        from_attributes = True 