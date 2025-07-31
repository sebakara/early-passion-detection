from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class GameBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    config: Dict[str, Any]
    difficulty_levels: Optional[List[str]] = None
    age_range: Dict[str, int]
    estimated_duration: Optional[int] = None
    max_players: int = 1
    requires_audio: bool = False
    requires_video: bool = False
    requires_microphone: bool = False
    passion_domains: List[str]

class GameCreate(GameBase):
    pass

class GameUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    config: Optional[Dict[str, Any]] = None
    difficulty_levels: Optional[List[str]] = None
    age_range: Optional[Dict[str, int]] = None
    estimated_duration: Optional[int] = None
    max_players: Optional[int] = None
    requires_audio: Optional[bool] = None
    requires_video: Optional[bool] = None
    requires_microphone: Optional[bool] = None
    passion_domains: Optional[List[str]] = None
    is_active: Optional[bool] = None
    is_beta: Optional[bool] = None
    version: Optional[str] = None

class GameInDB(GameBase):
    id: int
    is_active: bool
    is_beta: bool
    version: str
    total_plays: int
    average_rating: float
    average_completion_time: Optional[float] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Game(GameInDB):
    pass

class GameSessionCreate(BaseModel):
    child_id: int
    game_id: int
    difficulty_level: str = "beginner"

class GameSessionUpdate(BaseModel):
    status: Optional[str] = None
    completion_percentage: Optional[float] = None
    interactions: Optional[Dict[str, Any]] = None
    responses: Optional[Dict[str, Any]] = None
    emotional_reactions: Optional[Dict[str, Any]] = None
    attention_metrics: Optional[Dict[str, Any]] = None
    score: Optional[float] = None
    accuracy: Optional[float] = None
    speed_metrics: Optional[Dict[str, Any]] = None
    device_info: Optional[Dict[str, Any]] = None
    network_conditions: Optional[Dict[str, Any]] = None
    errors_encountered: Optional[List[str]] = None
    technical_issues: Optional[str] = None

class GameSessionInDB(BaseModel):
    id: int
    child_id: int
    game_id: int
    parent_id: int
    session_id: str
    difficulty_level: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    status: str
    completion_percentage: float
    interactions: Optional[Dict[str, Any]] = None
    responses: Optional[Dict[str, Any]] = None
    emotional_reactions: Optional[Dict[str, Any]] = None
    attention_metrics: Optional[Dict[str, Any]] = None
    score: Optional[float] = None
    accuracy: Optional[float] = None
    speed_metrics: Optional[Dict[str, Any]] = None
    device_info: Optional[Dict[str, Any]] = None
    network_conditions: Optional[Dict[str, Any]] = None
    errors_encountered: Optional[List[str]] = None
    technical_issues: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class GameSession(GameSessionInDB):
    pass 