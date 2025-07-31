from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta

from app.core.auth import get_current_active_user
from app.core.database import get_db
from app.models.user import User
from app.models.child import Child
from app.models.session import GameSession
from app.models.passion import PassionDomain, PassionInsight

router = APIRouter()

@router.get("/child/{child_id}/progress")
def get_child_progress(
    child_id: int,
    days: int = Query(30, description="Number of days to analyze"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get progress analytics for a child"""
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
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get sessions in date range
    sessions = db.query(GameSession).filter(
        GameSession.child_id == child_id,
        GameSession.created_at >= start_date,
        GameSession.created_at <= end_date
    ).all()
    
    # Calculate metrics
    total_sessions = len(sessions)
    completed_sessions = len([s for s in sessions if s.status == "completed"])
    total_play_time = sum([s.duration_seconds or 0 for s in sessions]) / 60  # Convert to minutes
    average_session_duration = total_play_time / total_sessions if total_sessions > 0 else 0
    
    # Get passion domains
    domains = db.query(PassionDomain).filter(
        PassionDomain.child_id == child_id,
        PassionDomain.is_active == True
    ).all()
    
    # Get recent insights
    insights = db.query(PassionInsight).filter(
        PassionInsight.child_id == child_id,
        PassionInsight.created_at >= start_date
    ).order_by(desc(PassionInsight.created_at)).limit(10).all()
    
    return {
        "child_id": child_id,
        "period_days": days,
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "completion_rate": (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0,
        "total_play_time_minutes": round(total_play_time, 2),
        "average_session_duration_minutes": round(average_session_duration, 2),
        "passion_domains_detected": len(domains),
        "recent_insights": len(insights),
        "top_domains": sorted(domains, key=lambda x: x.confidence_score, reverse=True)[:3] if domains else []
    }

@router.get("/child/{child_id}/activity-timeline")
def get_activity_timeline(
    child_id: int,
    days: int = Query(7, description="Number of days to analyze"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get activity timeline for a child"""
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
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get daily activity
    daily_activity = db.query(
        func.date(GameSession.created_at).label('date'),
        func.count(GameSession.id).label('sessions'),
        func.sum(GameSession.duration_seconds).label('total_duration')
    ).filter(
        GameSession.child_id == child_id,
        GameSession.created_at >= start_date,
        GameSession.created_at <= end_date
    ).group_by(func.date(GameSession.created_at)).all()
    
    # Format timeline data
    timeline = []
    for activity in daily_activity:
        timeline.append({
            "date": activity.date.isoformat(),
            "sessions": activity.sessions,
            "total_duration_minutes": round((activity.total_duration or 0) / 60, 2)
        })
    
    return {
        "child_id": child_id,
        "period_days": days,
        "timeline": timeline
    }

@router.get("/child/{child_id}/game-performance")
def get_game_performance(
    child_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get game performance analytics for a child"""
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
    
    # Get game performance data
    game_performance = db.query(
        GameSession.game_id,
        func.count(GameSession.id).label('total_sessions'),
        func.avg(GameSession.score).label('average_score'),
        func.avg(GameSession.accuracy).label('average_accuracy'),
        func.avg(GameSession.duration_seconds).label('average_duration')
    ).filter(
        GameSession.child_id == child_id,
        GameSession.status == "completed"
    ).group_by(GameSession.game_id).all()
    
    # Format performance data
    performance_data = []
    for perf in game_performance:
        performance_data.append({
            "game_id": perf.game_id,
            "total_sessions": perf.total_sessions,
            "average_score": round(perf.average_score or 0, 2),
            "average_accuracy": round(perf.average_accuracy or 0, 2),
            "average_duration_minutes": round((perf.average_duration or 0) / 60, 2)
        })
    
    return {
        "child_id": child_id,
        "game_performance": performance_data
    }

@router.get("/child/{child_id}/passion-evolution")
def get_passion_evolution(
    child_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get passion domain evolution over time"""
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
    
    # Get passion domains with timestamps
    domains = db.query(PassionDomain).filter(
        PassionDomain.child_id == child_id,
        PassionDomain.is_active == True
    ).order_by(PassionDomain.first_detected).all()
    
    # Format evolution data
    evolution = []
    for domain in domains:
        evolution.append({
            "domain": domain.domain,
            "first_detected": domain.first_detected.isoformat(),
            "initial_confidence": domain.confidence_score,
            "current_confidence": domain.confidence_score,
            "trend": domain.trend,
            "is_verified": domain.is_verified
        })
    
    return {
        "child_id": child_id,
        "passion_evolution": evolution
    }

@router.get("/dashboard/{child_id}")
def get_dashboard_data(
    child_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard data for a child"""
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
    
    # Get all relevant data
    sessions = db.query(GameSession).filter(GameSession.child_id == child_id).all()
    domains = db.query(PassionDomain).filter(
        PassionDomain.child_id == child_id,
        PassionDomain.is_active == True
    ).all()
    insights = db.query(PassionInsight).filter(
        PassionInsight.child_id == child_id
    ).order_by(desc(PassionInsight.created_at)).limit(5).all()
    
    # Calculate dashboard metrics
    total_play_time = sum([s.duration_seconds or 0 for s in sessions]) / 60
    completed_sessions = len([s for s in sessions if s.status == "completed"])
    total_sessions = len(sessions)
    
    # Get top performing games
    game_stats = {}
    for session in sessions:
        if session.game_id not in game_stats:
            game_stats[session.game_id] = {"sessions": 0, "total_score": 0}
        game_stats[session.game_id]["sessions"] += 1
        game_stats[session.game_id]["total_score"] += session.score or 0
    
    top_games = sorted(
        [{"game_id": k, "sessions": v["sessions"], "avg_score": v["total_score"] / v["sessions"]} 
         for k, v in game_stats.items()],
        key=lambda x: x["avg_score"],
        reverse=True
    )[:3]
    
    return {
        "child_id": child_id,
        "child_name": child.first_name,
        "age": child.age,
        "total_play_time_hours": round(total_play_time / 60, 2),
        "total_sessions": total_sessions,
        "completed_sessions": completed_sessions,
        "completion_rate": round((completed_sessions / total_sessions * 100) if total_sessions > 0 else 0, 1),
        "passion_domains_detected": len(domains),
        "top_domains": sorted(domains, key=lambda x: x.confidence_score, reverse=True)[:3] if domains else [],
        "recent_insights": insights,
        "top_games": top_games,
        "last_activity": child.last_activity.isoformat() if child.last_activity else None
    } 