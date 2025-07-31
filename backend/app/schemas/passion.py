from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class PassionDomainBase(BaseModel):
    domain: str
    confidence_score: float
    strength_level: str
    detection_method: str
    model_version: Optional[str] = None
    data_points_used: int = 0
    supporting_evidence: Optional[Dict[str, Any]] = None
    games_played: Optional[List[str]] = None
    behavioral_patterns: Optional[Dict[str, Any]] = None
    trend: Optional[str] = None
    recommended_activities: Optional[List[str]] = None
    difficulty_progression: Optional[Dict[str, Any]] = None
    is_active: bool = True
    is_verified: bool = False

class PassionDomainCreate(PassionDomainBase):
    child_id: int

class PassionDomainUpdate(BaseModel):
    confidence_score: Optional[float] = None
    strength_level: Optional[str] = None
    supporting_evidence: Optional[Dict[str, Any]] = None
    games_played: Optional[List[str]] = None
    behavioral_patterns: Optional[Dict[str, Any]] = None
    trend: Optional[str] = None
    recommended_activities: Optional[List[str]] = None
    difficulty_progression: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None

class PassionDomainInDB(PassionDomainBase):
    id: int
    child_id: int
    first_detected: datetime
    last_updated: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PassionDomain(PassionDomainInDB):
    pass

class PassionInsightBase(BaseModel):
    insight_type: str
    title: str
    description: str
    data: Optional[Dict[str, Any]] = None
    related_domains: Optional[List[str]] = None
    importance_score: float = 0.5
    is_highlighted: bool = False
    notify_parent: bool = False

class PassionInsightCreate(PassionInsightBase):
    child_id: int

class PassionInsightUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    related_domains: Optional[List[str]] = None
    importance_score: Optional[float] = None
    is_highlighted: Optional[bool] = None
    notify_parent: Optional[bool] = None
    parent_notified: Optional[bool] = None

class PassionInsightInDB(PassionInsightBase):
    id: int
    child_id: int
    parent_notified: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class PassionInsight(PassionInsightInDB):
    pass

class PassionAnalysis(BaseModel):
    child_id: int
    domains: List[PassionDomain]
    insights: List[PassionInsight]
    overall_confidence: float
    recommended_next_activities: List[str]
    development_trends: Dict[str, str]
    last_updated: datetime

class PassionRecommendation(BaseModel):
    domain: str
    confidence: float
    activities: List[str]
    difficulty_level: str
    estimated_duration: int
    description: str
    why_recommended: str 