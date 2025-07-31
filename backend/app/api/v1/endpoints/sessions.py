from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
import uuid

from app.core.auth import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.game import Game
from app.models.session import GameSession
from app.schemas.game import GameSessionCreate, GameSession as GameSessionSchema, GameSessionUpdate

router = APIRouter()

@router.post("/", response_model=GameSessionSchema)
def create_session(
    session_data: GameSessionCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new game session"""
    # Verify child access
    child = db.query(Child).filter(Child.id == session_data.child_id).first()
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    if child.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Verify game exists
    game = db.query(Game).filter(Game.id == session_data.game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Check if child has parental consent
    if not child.parental_consent_given:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parental consent required for data collection"
        )
    
    # Create session
    session_id = str(uuid.uuid4())
    db_session = GameSession(
        child_id=session_data.child_id,
        game_id=session_data.game_id,
        parent_id=current_user.id,
        session_id=session_id,
        difficulty_level=session_data.difficulty_level,
        status="active"
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    # Update child's last activity
    child.last_activity = datetime.now()
    db.commit()
    
    return db_session

@router.get("/", response_model=List[GameSessionSchema])
def get_sessions(
    child_id: int = None,
    game_id: int = None,
    status: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get game sessions with optional filters"""
    query = db.query(GameSession)
    
    if child_id:
        # Verify child access
        child = db.query(Child).filter(Child.id == child_id).first()
        if not child or child.parent_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        query = query.filter(GameSession.child_id == child_id)
    else:
        # Get all sessions for user's children
        children = db.query(Child).filter(Child.parent_id == current_user.id).all()
        child_ids = [child.id for child in children]
        query = query.filter(GameSession.child_id.in_(child_ids))
    
    if game_id:
        query = query.filter(GameSession.game_id == game_id)
    
    if status:
        query = query.filter(GameSession.status == status)
    
    sessions = query.order_by(GameSession.created_at.desc()).all()
    return sessions

@router.get("/{session_id}", response_model=GameSessionSchema)
def get_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a specific game session"""
    session = db.query(GameSession).filter(GameSession.session_id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Verify access
    if session.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return session

@router.put("/{session_id}", response_model=GameSessionSchema)
def update_session(
    session_id: str,
    session_update: GameSessionUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a game session (for data collection)"""
    session = db.query(GameSession).filter(GameSession.session_id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Verify access
    if session.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update fields
    update_data = session_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(session, field, value)
    
    # If session is being completed, calculate duration
    if session_update.status == "completed" and session.started_at:
        session.completed_at = datetime.now()
        session.duration_seconds = (session.completed_at - session.started_at).total_seconds()
        
        # Update child's total play time
        child = db.query(Child).filter(Child.id == session.child_id).first()
        if child:
            child.total_play_time += session.duration_seconds / 60  # Convert to minutes
            child.sessions_completed += 1
            child.last_activity = datetime.now()
    
    db.commit()
    db.refresh(session)
    
    return session

@router.delete("/{session_id}")
def delete_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a game session"""
    session = db.query(GameSession).filter(GameSession.session_id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    # Verify access
    if session.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(session)
    db.commit()
    
    return {"message": "Session deleted successfully"}

@router.post("/{session_id}/complete")
def complete_session(
    session_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mark a session as completed"""
    session = db.query(GameSession).filter(GameSession.session_id == session_id).first()
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    if session.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    session.status = "completed"
    session.completed_at = datetime.now()
    session.completion_percentage = 100.0
    
    if session.started_at:
        session.duration_seconds = (session.completed_at - session.started_at).total_seconds()
    
    # Update child's stats
    child = db.query(Child).filter(Child.id == session.child_id).first()
    if child:
        child.total_play_time += session.duration_seconds / 60 if session.duration_seconds else 0
        child.sessions_completed += 1
        child.last_activity = datetime.now()
    
    db.commit()
    
    return {"message": "Session completed successfully"} 