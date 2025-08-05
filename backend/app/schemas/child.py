from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class ChildBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    date_of_birth: datetime
    gender: Optional[str] = None
    initial_interests: Optional[List[str]] = None
    favorite_colors: Optional[List[str]] = None
    favorite_activities: Optional[List[str]] = None
    learning_style: Optional[str] = None

class ChildCreate(ChildBase):
    @validator('date_of_birth')
    def validate_age(cls, v):
        age = (datetime.now() - v).days / 365.25
        if age < 3 or age > 12:
            raise ValueError('Child must be between 3 and 12 years old')
        return v

class ChildUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    initial_interests: Optional[List[str]] = None
    favorite_colors: Optional[List[str]] = None
    favorite_activities: Optional[List[str]] = None
    learning_style: Optional[str] = None

class ChildInDB(ChildBase):
    id: int
    user_id: int
    parent_id: int
    age: int
    current_level: str
    total_play_time: float
    sessions_completed: int
    parental_consent_given: bool
    consent_date: Optional[datetime] = None
    data_sharing_preferences: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Child(ChildInDB):
    pass

class ChildSummary(BaseModel):
    id: int
    first_name: str
    age: int
    current_level: str
    total_play_time: float
    sessions_completed: int
    last_activity: Optional[datetime] = None 