from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.auth import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.schemas.child import ChildCreate, Child as ChildSchema, ChildUpdate, ChildSummary

router = APIRouter()

@router.post("/", response_model=ChildSchema)
def create_child(child: ChildCreate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Create a new child profile"""
    if not current_user.is_parent:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only parents can create child profiles"
        )
    
    # Calculate age
    age = int((datetime.now() - child.date_of_birth).days / 365.25)
    
    # Create child profile
    db_child = Child(
        user_id=current_user.id,
        parent_id=current_user.id,
        first_name=child.first_name,
        last_name=child.last_name,
        date_of_birth=child.date_of_birth,
        age=age,
        gender=child.gender,
        initial_interests=child.initial_interests,
        favorite_colors=child.favorite_colors,
        favorite_activities=child.favorite_activities,
        learning_style=child.learning_style
    )
    
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    
    return db_child

@router.get("/", response_model=List[ChildSummary])
def get_children(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get all children for the current user"""
    if current_user.is_parent:
        children = db.query(Child).filter(Child.parent_id == current_user.id).all()
    else:
        # For children, return their own profile
        children = db.query(Child).filter(Child.user_id == current_user.id).all()
    
    return children

@router.get("/{child_id}", response_model=ChildSchema)
def get_child(child_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Get a specific child profile"""
    child = db.query(Child).filter(Child.id == child_id).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    # Check access permissions
    if current_user.is_parent:
        if child.parent_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    else:
        if child.user_id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
    
    return child

@router.put("/{child_id}", response_model=ChildSchema)
def update_child(child_id: int, child_update: ChildUpdate, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Update a child profile"""
    child = db.query(Child).filter(Child.id == child_id).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    # Check access permissions
    if child.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    # Update fields
    update_data = child_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(child, field, value)
    
    db.commit()
    db.refresh(child)
    
    return child

@router.delete("/{child_id}")
def delete_child(child_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Delete a child profile"""
    child = db.query(Child).filter(Child.id == child_id).first()
    
    if not child:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Child not found"
        )
    
    # Check access permissions
    if child.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    db.delete(child)
    db.commit()
    
    return {"message": "Child profile deleted successfully"}

@router.post("/{child_id}/consent")
def give_parental_consent(child_id: int, current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Give parental consent for data collection"""
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
    
    child.parental_consent_given = True
    child.consent_date = datetime.now()
    
    db.commit()
    
    return {"message": "Parental consent given successfully"} 