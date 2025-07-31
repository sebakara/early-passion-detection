from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.auth import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.passion import PassionDomain, PassionInsight
from app.schemas.passion import (
    PassionDomain as PassionDomainSchema,
    PassionInsight as PassionInsightSchema,
    PassionAnalysis,
    PassionRecommendation
)

router = APIRouter()

@router.get("/domains/{child_id}", response_model=List[PassionDomainSchema])
def get_passion_domains(
    child_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detected passion domains for a child"""
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
    
    domains = db.query(PassionDomain).filter(
        PassionDomain.child_id == child_id,
        PassionDomain.is_active == True
    ).all()
    
    return domains

@router.get("/insights/{child_id}", response_model=List[PassionInsightSchema])
def get_passion_insights(
    child_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get passion insights for a child"""
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
    
    insights = db.query(PassionInsight).filter(
        PassionInsight.child_id == child_id
    ).order_by(PassionInsight.created_at.desc()).all()
    
    return insights

@router.get("/recommendations/{child_id}", response_model=List[PassionRecommendation])
def get_recommendations(
    child_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get personalized recommendations for a child"""
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
    
    # Get passion domains
    domains = db.query(PassionDomain).filter(
        PassionDomain.child_id == child_id,
        PassionDomain.is_active == True
    ).all()
    
    # Generate recommendations based on detected domains
    recommendations = []
    for domain in domains:
        if domain.confidence_score > 0.6:  # Only recommend for strong detections
            recommendation = PassionRecommendation(
                domain=domain.domain,
                confidence=domain.confidence_score,
                activities=domain.recommended_activities or [],
                difficulty_level=domain.difficulty_progression.get('current', 'beginner') if domain.difficulty_progression else 'beginner',
                estimated_duration=30,  # Default 30 minutes
                description=f"Activities to explore {domain.domain} interests",
                why_recommended=f"Based on strong patterns in {domain.domain} activities"
            )
            recommendations.append(recommendation)
    
    return recommendations

@router.post("/domains/{domain_id}/verify")
def verify_passion_domain(
    domain_id: int,
    verified: bool,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Verify a passion domain detection (parent feedback)"""
    domain = db.query(PassionDomain).filter(PassionDomain.id == domain_id).first()
    
    if not domain:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Passion domain not found"
        )
    
    # Verify child access
    child = db.query(Child).filter(Child.id == domain.child_id).first()
    if not child or child.parent_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    domain.is_verified = verified
    db.commit()
    
    return {"message": f"Passion domain {'verified' if verified else 'marked as unverified'}"}

@router.get("/summary/{child_id}")
def get_passion_summary(
    child_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a summary of passion detection results"""
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
    
    # Get active domains
    domains = db.query(PassionDomain).filter(
        PassionDomain.child_id == child_id,
        PassionDomain.is_active == True
    ).all()
    
    # Get recent insights
    insights = db.query(PassionInsight).filter(
        PassionInsight.child_id == child_id
    ).order_by(PassionInsight.created_at.desc()).limit(5).all()
    
    # Calculate summary statistics
    total_domains = len(domains)
    high_confidence_domains = len([d for d in domains if d.confidence_score > 0.7])
    verified_domains = len([d for d in domains if d.is_verified])
    
    return {
        "child_id": child_id,
        "total_domains_detected": total_domains,
        "high_confidence_domains": high_confidence_domains,
        "verified_domains": verified_domains,
        "top_domains": sorted(domains, key=lambda x: x.confidence_score, reverse=True)[:3],
        "recent_insights": insights,
        "last_analysis": max([d.last_updated for d in domains]) if domains else None
    } 