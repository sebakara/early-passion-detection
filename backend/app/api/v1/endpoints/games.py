from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.auth import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.models.game import Game
from app.models.child import Child
from app.schemas.game import Game as GameSchema, GameCreate, GameUpdate

router = APIRouter()

@router.get("/", response_model=List[GameSchema])
def get_games(
    category: Optional[str] = Query(None, description="Filter by game category"),
    age_min: Optional[int] = Query(None, description="Minimum age filter"),
    age_max: Optional[int] = Query(None, description="Maximum age filter"),
    difficulty: Optional[str] = Query(None, description="Difficulty level"),
    passion_domain: Optional[str] = Query(None, description="Filter by passion domain"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get available games with optional filters"""
    query = db.query(Game).filter(Game.is_active == True)
    
    if category:
        query = query.filter(Game.category == category)
    
    if passion_domain:
        query = query.filter(Game.passion_domains.contains([passion_domain]))
    
    if age_min is not None:
        query = query.filter(Game.age_range['min'] >= age_min)
    
    if age_max is not None:
        query = query.filter(Game.age_range['max'] <= age_max)
    
    games = query.all()
    return games

@router.get("/recommended", response_model=List[GameSchema])
def get_recommended_games(
    child_id: int,
    limit: int = Query(5, description="Number of recommendations"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized game recommendations for a child"""
    # Verify child access
    child = db.query(Child).filter(Child.id == child_id).first()
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
    
    # Simple recommendation logic (can be enhanced with ML)
    # For now, return games appropriate for the child's age
    recommended_games = db.query(Game).filter(
        Game.is_active == True,
        Game.age_range['min'] <= child.age,
        Game.age_range['max'] >= child.age
    ).limit(limit).all()
    
    return recommended_games

@router.get("/{game_id}", response_model=GameSchema)
def get_game(game_id: int, db: Session = Depends(get_db)):
    """Get a specific game by ID"""
    game = db.query(Game).filter(Game.id == game_id).first()
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    return game

@router.post("/", response_model=GameSchema)
def create_game(
    game: GameCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new game (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    db_game = Game(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    
    return db_game

@router.put("/{game_id}", response_model=GameSchema)
def update_game(
    game_id: int,
    game_update: GameUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a game (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    update_data = game_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(game, field, value)
    
    db.commit()
    db.refresh(game)
    
    return game

@router.delete("/{game_id}")
def delete_game(
    game_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a game (admin only)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    game = db.query(Game).filter(Game.id == game_id).first()
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    db.delete(game)
    db.commit()
    
    return {"message": "Game deleted successfully"}

@router.get("/categories/list")
def get_game_categories():
    """Get list of available game categories"""
    categories = [
        "art",
        "music", 
        "science",
        "sports",
        "leadership",
        "language",
        "logic"
    ]
    return {"categories": categories}

@router.get("/domains/list")
def get_passion_domains():
    """Get list of passion domains"""
    domains = [
        "art_creativity",
        "music_rhythm", 
        "science_discovery",
        "sports_movement",
        "leadership_social",
        "language_communication",
        "logic_mathematics"
    ]
    return {"domains": domains} 