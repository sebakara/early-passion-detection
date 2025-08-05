from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.question import Question, QuestionResponse, TalentAssessment
from app.models.child import Child
from app.schemas.question import (
    Question as QuestionSchema,
    QuestionCreate,
    QuestionResponse as QuestionResponseSchema,
    QuestionResponseCreate,
    TalentAssessment as TalentAssessmentSchema,
    TalentAssessmentCreate,
    QuestionSet
)
from app.ml.passion_detector import analyze_talent_responses

router = APIRouter()

@router.get("/", response_model=List[QuestionSchema])
def get_questions(
    category: Optional[str] = None,
    talent_domain: Optional[str] = None,
    age: Optional[int] = None,
    difficulty: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get questions with optional filtering"""
    query = db.query(Question).filter(Question.is_active == True)
    
    if category:
        query = query.filter(Question.category == category)
    if talent_domain:
        query = query.filter(Question.talent_domain == talent_domain)
    if age:
        query = query.filter(Question.min_age <= age, Question.max_age >= age)
    if difficulty:
        query = query.filter(Question.difficulty_level == difficulty)
    
    return query.all()

@router.get("/categories", response_model=List[str])
def get_question_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all available question categories"""
    categories = db.query(Question.category).distinct().all()
    return [cat[0] for cat in categories]

@router.get("/talent-domains", response_model=List[str])
def get_talent_domains(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get all available talent domains"""
    domains = db.query(Question.talent_domain).distinct().all()
    return [domain[0] for domain in domains]

@router.get("/assessment/{child_id}", response_model=QuestionSet)
def get_assessment_questions(
    child_id: int,
    category: Optional[str] = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get a set of questions for talent assessment"""
    # Check if child exists and user has access
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    if child.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Calculate child's age
    age = int((datetime.now() - child.date_of_birth).days / 365.25)
    
    # Get questions appropriate for the child's age
    query = db.query(Question).filter(
        Question.is_active == True,
        Question.min_age <= age,
        Question.max_age >= age
    )
    
    if category:
        query = query.filter(Question.category == category)
    
    questions = query.limit(10).all()  # Limit to 10 questions for assessment
    
    return QuestionSet(
        id=1,
        name=f"Talent Assessment for {child.first_name}",
        description="Discover your child's natural talents and interests",
        category=category or "general",
        questions=questions,
        estimated_duration=len(questions) * 2,  # 2 minutes per question
        target_age_range={"min": age - 1, "max": age + 1}
    )

@router.post("/response", response_model=QuestionResponseSchema)
def submit_response(
    response: QuestionResponseCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit a response to a question"""
    # Verify child exists and user has access
    child = db.query(Child).filter(Child.id == response.child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    if child.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Verify question exists
    question = db.query(Question).filter(Question.id == response.question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Calculate score based on answer and scoring weights
    score = None
    if question.scoring_weights and response.answer in question.scoring_weights:
        score = question.scoring_weights[response.answer]
    
    # Create response
    db_response = QuestionResponse(
        child_id=response.child_id,
        question_id=response.question_id,
        session_id=response.session_id,
        answer=response.answer,
        response_time=response.response_time,
        confidence_level=response.confidence_level,
        score=score,
        talent_indicators={"domain": question.talent_domain, "score": score}
    )
    
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    
    return db_response

@router.post("/assessment/{child_id}/analyze", response_model=TalentAssessmentSchema)
def analyze_talents(
    child_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Analyze child's responses and generate talent assessment"""
    # Verify child exists and user has access
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    if child.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Get recent responses for this child
    responses = db.query(QuestionResponse).filter(
        QuestionResponse.child_id == child_id
    ).order_by(QuestionResponse.created_at.desc()).limit(20).all()
    
    if not responses:
        raise HTTPException(status_code=400, detail="No responses found for analysis")
    
    # Analyze responses using ML model
    analysis_result = analyze_talent_responses(responses, child)
    
    # Create talent assessment
    assessment = TalentAssessment(
        child_id=child_id,
        talent_domains=analysis_result["talent_domains"],
        primary_talent=analysis_result["primary_talent"],
        secondary_talents=analysis_result["secondary_talents"],
        confidence_score=analysis_result["confidence_score"],
        behavioral_patterns=analysis_result["behavioral_patterns"],
        response_patterns=analysis_result["response_patterns"],
        interest_indicators=analysis_result["interest_indicators"],
        recommended_activities=analysis_result["recommended_activities"],
        development_path=analysis_result["development_path"]
    )
    
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    return assessment

@router.get("/assessment/{child_id}/history", response_model=List[TalentAssessmentSchema])
def get_assessment_history(
    child_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get assessment history for a child"""
    # Verify child exists and user has access
    child = db.query(Child).filter(Child.id == child_id).first()
    if not child:
        raise HTTPException(status_code=404, detail="Child not found")
    
    if child.parent_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    assessments = db.query(TalentAssessment).filter(
        TalentAssessment.child_id == child_id
    ).order_by(TalentAssessment.assessment_date.desc()).all()
    
    return assessments 