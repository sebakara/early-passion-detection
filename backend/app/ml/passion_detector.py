import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import joblib
import os

from app.models.session import GameSession
from app.models.passion import PassionDomain, PassionInsight
from app.models.game import Game
from app.models.question import QuestionResponse
from app.models.child import Child
from app.core.config import settings

# Talent domain definitions with characteristics
TALENT_DOMAINS = {
    "artistic_creativity": {
        "name": "Artistic Creativity",
        "description": "Natural talent for visual arts, design, and creative expression",
        "indicators": ["visual thinking", "color sensitivity", "creative problem solving", "imagination"],
        "activities": ["drawing", "painting", "sculpture", "digital art", "crafts"],
        "careers": ["artist", "designer", "architect", "animator", "photographer"]
    },
    "musical_rhythm": {
        "name": "Musical Rhythm",
        "description": "Natural ability to understand and create music",
        "indicators": ["rhythm awareness", "pitch recognition", "musical memory", "emotional response to music"],
        "activities": ["singing", "playing instruments", "dancing", "music composition", "rhythm games"],
        "careers": ["musician", "composer", "music teacher", "sound engineer", "performer"]
    },
    "logical_mathematics": {
        "name": "Logical Mathematics",
        "description": "Strong analytical and mathematical thinking",
        "indicators": ["pattern recognition", "logical reasoning", "number sense", "problem solving"],
        "activities": ["puzzles", "math games", "coding", "science experiments", "strategy games"],
        "careers": ["engineer", "scientist", "mathematician", "programmer", "analyst"]
    },
    "sports_movement": {
        "name": "Sports & Movement",
        "description": "Natural athletic ability and physical coordination",
        "indicators": ["coordination", "balance", "speed", "strength", "teamwork"],
        "activities": ["sports", "dance", "gymnastics", "martial arts", "outdoor activities"],
        "careers": ["athlete", "coach", "physical therapist", "fitness trainer", "dance instructor"]
    },
    "language_communication": {
        "name": "Language & Communication",
        "description": "Strong verbal and written communication skills",
        "indicators": ["vocabulary", "storytelling", "reading comprehension", "verbal expression"],
        "activities": ["reading", "writing", "storytelling", "debate", "public speaking"],
        "careers": ["writer", "journalist", "teacher", "lawyer", "public relations"]
    },
    "social_leadership": {
        "name": "Social Leadership",
        "description": "Natural leadership and social skills",
        "indicators": ["empathy", "teamwork", "leadership", "conflict resolution", "social awareness"],
        "activities": ["group activities", "team sports", "community service", "leadership roles"],
        "careers": ["manager", "teacher", "counselor", "politician", "entrepreneur"]
    },
    "scientific_discovery": {
        "name": "Scientific Discovery",
        "description": "Curiosity and analytical thinking about the natural world",
        "indicators": ["curiosity", "observation", "experimentation", "critical thinking"],
        "activities": ["science experiments", "nature exploration", "building models", "research projects"],
        "careers": ["scientist", "researcher", "doctor", "veterinarian", "environmentalist"]
    },
    "technology_innovation": {
        "name": "Technology & Innovation",
        "description": "Interest in technology and innovative problem solving",
        "indicators": ["tech curiosity", "problem solving", "innovation", "adaptability"],
        "activities": ["coding", "robotics", "electronics", "gaming", "app development"],
        "careers": ["software engineer", "data scientist", "product manager", "entrepreneur", "researcher"]
    }
}

def analyze_talent_responses(responses: List[QuestionResponse], child: Child) -> Dict[str, Any]:
    """
    Analyze question responses to detect talent domains and generate assessment
    """
    if not responses:
        return _generate_default_assessment(child)
    
    # Calculate age
    age = int((datetime.now() - child.date_of_birth).days / 365.25)
    
    # Initialize talent domain scores
    talent_scores = {domain: 0.0 for domain in TALENT_DOMAINS.keys()}
    response_count = {domain: 0 for domain in TALENT_DOMAINS.keys()}
    
    # Analyze each response
    total_response_time = 0
    confidence_scores = []
    
    for response in responses:
        if response.talent_indicators and "domain" in response.talent_indicators:
            domain = response.talent_indicators["domain"]
            if domain in talent_scores:
                # Add score (normalize to 0-1 range)
                score = response.score or 0.5
                talent_scores[domain] += score
                response_count[domain] += 1
        
        # Track response patterns
        if response.response_time:
            total_response_time += response.response_time
        if response.confidence_level:
            confidence_scores.append(response.confidence_level)
    
    # Calculate average scores for each domain
    for domain in talent_scores:
        if response_count[domain] > 0:
            talent_scores[domain] = talent_scores[domain] / response_count[domain]
        else:
            # Use child's initial interests as a hint
            if child.initial_interests:
                for interest in child.initial_interests:
                    if _interest_matches_domain(interest, domain):
                        talent_scores[domain] = 0.6  # Moderate interest
    
    # Determine primary and secondary talents
    sorted_talents = sorted(talent_scores.items(), key=lambda x: x[1], reverse=True)
    primary_talent = sorted_talents[0][0] if sorted_talents[0][1] > 0.5 else None
    secondary_talents = [talent[0] for talent in sorted_talents[1:4] if talent[1] > 0.4]
    
    # Calculate confidence score
    confidence_score = _calculate_confidence_score(responses, talent_scores)
    
    # Analyze behavioral patterns
    behavioral_patterns = _analyze_behavioral_patterns(responses, total_response_time, confidence_scores)
    
    # Analyze response patterns
    response_patterns = _analyze_response_patterns(responses)
    
    # Generate interest indicators
    interest_indicators = _generate_interest_indicators(child, talent_scores)
    
    # Generate recommendations
    recommended_activities = _generate_recommendations(primary_talent, secondary_talents, age)
    
    # Generate development path
    development_path = _generate_development_path(primary_talent, age)
    
    return {
        "talent_domains": talent_scores,
        "primary_talent": primary_talent,
        "secondary_talents": secondary_talents,
        "confidence_score": confidence_score,
        "behavioral_patterns": behavioral_patterns,
        "response_patterns": response_patterns,
        "interest_indicators": interest_indicators,
        "recommended_activities": recommended_activities,
        "development_path": development_path
    }

def _interest_matches_domain(interest: str, domain: str) -> bool:
    """Check if an interest matches a talent domain"""
    interest_lower = interest.lower()
    domain_info = TALENT_DOMAINS.get(domain, {})
    
    # Check against domain activities
    for activity in domain_info.get("activities", []):
        if activity.lower() in interest_lower:
            return True
    
    # Check against domain indicators
    for indicator in domain_info.get("indicators", []):
        if indicator.lower() in interest_lower:
            return True
    
    return False

def _calculate_confidence_score(responses: List[QuestionResponse], talent_scores: Dict[str, float]) -> float:
    """Calculate confidence in the assessment"""
    if not responses:
        return 0.3
    
    # Factors affecting confidence:
    # 1. Number of responses
    response_factor = min(len(responses) / 10.0, 1.0)
    
    # 2. Consistency of scores
    score_variance = np.var(list(talent_scores.values()))
    consistency_factor = max(0, 1 - score_variance)
    
    # 3. Response quality (confidence levels)
    avg_confidence = 0.5  # Default
    if any(r.confidence_level for r in responses):
        confidences = [r.confidence_level for r in responses if r.confidence_level]
        avg_confidence = sum(confidences) / len(confidences) / 10.0
    
    # Weighted average
    confidence_score = (response_factor * 0.4 + consistency_factor * 0.4 + avg_confidence * 0.2)
    return min(confidence_score, 1.0)

def _analyze_behavioral_patterns(responses: List[QuestionResponse], total_response_time: float, confidence_scores: List[float]) -> Dict[str, Any]:
    """Analyze behavioral patterns from responses"""
    patterns = {
        "response_speed": "normal",
        "confidence_level": "moderate",
        "engagement_level": "moderate",
        "consistency": "moderate"
    }
    
    if responses:
        avg_response_time = total_response_time / len(responses)
        if avg_response_time < 10:
            patterns["response_speed"] = "fast"
        elif avg_response_time > 30:
            patterns["response_speed"] = "slow"
        
        if confidence_scores:
            avg_confidence = sum(confidence_scores) / len(confidence_scores)
            if avg_confidence > 7:
                patterns["confidence_level"] = "high"
            elif avg_confidence < 4:
                patterns["confidence_level"] = "low"
    
    return patterns

def _analyze_response_patterns(responses: List[QuestionResponse]) -> Dict[str, Any]:
    """Analyze response patterns and consistency"""
    patterns = {
        "total_responses": len(responses),
        "response_consistency": "moderate",
        "learning_curve": "stable"
    }
    
    if len(responses) >= 5:
        # Check for improvement over time
        recent_scores = [r.score for r in responses[-5:] if r.score]
        early_scores = [r.score for r in responses[:5] if r.score]
        
        if recent_scores and early_scores:
            recent_avg = sum(recent_scores) / len(recent_scores)
            early_avg = sum(early_scores) / len(early_scores)
            
            if recent_avg > early_avg * 1.2:
                patterns["learning_curve"] = "improving"
            elif recent_avg < early_avg * 0.8:
                patterns["learning_curve"] = "declining"
    
    return patterns

def _generate_interest_indicators(child: Child, talent_scores: Dict[str, float]) -> Dict[str, Any]:
    """Generate interest indicators based on child data and talent scores"""
    indicators = {
        "strong_interests": [],
        "moderate_interests": [],
        "potential_interests": []
    }
    
    # Add interests from child profile
    if child.initial_interests:
        indicators["strong_interests"].extend(child.initial_interests)
    
    if child.favorite_activities:
        indicators["moderate_interests"].extend(child.favorite_activities)
    
    # Add interests based on talent scores
    for domain, score in talent_scores.items():
        if score > 0.7:
            domain_info = TALENT_DOMAINS.get(domain, {})
            indicators["strong_interests"].extend(domain_info.get("activities", [])[:2])
        elif score > 0.5:
            domain_info = TALENT_DOMAINS.get(domain, {})
            indicators["moderate_interests"].extend(domain_info.get("activities", [])[:1])
    
    return indicators

def _generate_recommendations(primary_talent: str, secondary_talents: List[str], age: int) -> List[str]:
    """Generate activity recommendations based on detected talents"""
    recommendations = []
    
    if primary_talent and primary_talent in TALENT_DOMAINS:
        domain_info = TALENT_DOMAINS[primary_talent]
        recommendations.extend(domain_info.get("activities", [])[:3])
    
    for talent in secondary_talents[:2]:  # Limit to 2 secondary talents
        if talent in TALENT_DOMAINS:
            domain_info = TALENT_DOMAINS[talent]
            recommendations.extend(domain_info.get("activities", [])[:2])
    
    # Add age-appropriate activities
    age_activities = _get_age_appropriate_activities(age)
    recommendations.extend(age_activities[:3])
    
    return list(set(recommendations))  # Remove duplicates

def _generate_development_path(primary_talent: str, age: int) -> Dict[str, Any]:
    """Generate a development path for the child's primary talent"""
    if not primary_talent or primary_talent not in TALENT_DOMAINS:
        return {"current_stage": "exploration", "next_steps": ["try different activities"]}
    
    domain_info = TALENT_DOMAINS[primary_talent]
    
    # Define development stages based on age
    if age < 6:
        stage = "discovery"
        focus = "exploration and play"
    elif age < 9:
        stage = "development"
        focus = "skill building and practice"
    else:
        stage = "refinement"
        focus = "advanced techniques and specialization"
    
    return {
        "current_stage": stage,
        "focus_area": focus,
        "primary_talent": domain_info["name"],
        "career_paths": domain_info.get("careers", []),
        "next_steps": domain_info.get("activities", [])[:3]
    }

def _get_age_appropriate_activities(age: int) -> List[str]:
    """Get age-appropriate activities"""
    if age < 5:
        return ["coloring", "building blocks", "singing", "dancing", "outdoor play"]
    elif age < 8:
        return ["arts and crafts", "music lessons", "sports", "reading", "puzzles"]
    else:
        return ["advanced art projects", "instrument practice", "team sports", "writing", "science projects"]

def _generate_default_assessment(child: Child) -> Dict[str, Any]:
    """Generate a default assessment when no responses are available"""
    return {
        "talent_domains": {domain: 0.3 for domain in TALENT_DOMAINS.keys()},
        "primary_talent": None,
        "secondary_talents": [],
        "confidence_score": 0.2,
        "behavioral_patterns": {"response_speed": "unknown", "confidence_level": "unknown"},
        "response_patterns": {"total_responses": 0, "response_consistency": "unknown"},
        "interest_indicators": {
            "strong_interests": child.initial_interests or [],
            "moderate_interests": child.favorite_activities or [],
            "potential_interests": []
        },
        "recommended_activities": _get_age_appropriate_activities(int((datetime.now() - child.date_of_birth).days / 365.25)),
        "development_path": {"current_stage": "exploration", "next_steps": ["start assessments"]}
    }

class PassionDetector:
    """Machine learning system for detecting children's passions and talents"""
    
    def __init__(self):
        self.domains = [
            "art_creativity",
            "music_rhythm", 
            "science_discovery",
            "sports_movement",
            "leadership_social",
            "language_communication",
            "logic_mathematics"
        ]
        
        self.domain_keywords = {
            "art_creativity": ["drawing", "painting", "colors", "creative", "art", "design", "imagination"],
            "music_rhythm": ["music", "rhythm", "sound", "singing", "dancing", "melody", "beat"],
            "science_discovery": ["experiment", "discovery", "science", "nature", "observation", "curiosity"],
            "sports_movement": ["movement", "sports", "physical", "coordination", "team", "exercise"],
            "leadership_social": ["leadership", "social", "communication", "teamwork", "friends", "group"],
            "language_communication": ["language", "words", "reading", "writing", "communication", "story"],
            "logic_mathematics": ["logic", "math", "numbers", "puzzle", "pattern", "problem", "thinking"]
        }
        
        self.models = {}
        self.load_models()
    
    def load_models(self):
        """Load pre-trained ML models"""
        model_path = settings.MODEL_PATH
        for domain in self.domains:
            model_file = os.path.join(model_path, f"{domain}_model.pkl")
            if os.path.exists(model_file):
                try:
                    self.models[domain] = joblib.load(model_file)
                except Exception as e:
                    print(f"Error loading model for {domain}: {e}")
    
    def extract_features(self, sessions: List[GameSession], games: List[Game]) -> Dict[str, Any]:
        """Extract features from game sessions for passion detection"""
        features = {}
        
        # Session-level features
        features['total_sessions'] = len(sessions)
        features['completed_sessions'] = len([s for s in sessions if s.status == "completed"])
        features['completion_rate'] = features['completed_sessions'] / features['total_sessions'] if features['total_sessions'] > 0 else 0
        
        # Time-based features
        total_duration = sum([s.duration_seconds or 0 for s in sessions])
        features['total_play_time'] = total_duration / 60  # Convert to minutes
        features['avg_session_duration'] = total_duration / len(sessions) if sessions else 0
        
        # Performance features
        scores = [s.score for s in sessions if s.score is not None]
        features['avg_score'] = np.mean(scores) if scores else 0
        features['max_score'] = max(scores) if scores else 0
        
        # Game category preferences
        game_categories = {}
        for session in sessions:
            game = next((g for g in games if g.id == session.game_id), None)
            if game:
                category = game.category
                game_categories[category] = game_categories.get(category, 0) + 1
        
        features['category_preferences'] = game_categories
        
        # Behavioral features
        response_times = []
        accuracy_scores = []
        
        for session in sessions:
            if session.speed_metrics:
                response_times.extend(session.speed_metrics.get('response_times', []))
            if session.accuracy is not None:
                accuracy_scores.append(session.accuracy)
        
        features['avg_response_time'] = np.mean(response_times) if response_times else 0
        features['avg_accuracy'] = np.mean(accuracy_scores) if accuracy_scores else 0
        
        # Emotional engagement
        emotional_scores = []
        for session in sessions:
            if session.emotional_reactions:
                # Extract positive emotions (excitement, joy, engagement)
                positive_emotions = session.emotional_reactions.get('positive', 0)
                emotional_scores.append(positive_emotions)
        
        features['emotional_engagement'] = np.mean(emotional_scores) if emotional_scores else 0
        
        return features
    
    def rule_based_detection(self, features: Dict[str, Any], child_interests: List[str] = None) -> Dict[str, float]:
        """Rule-based passion detection using heuristics"""
        scores = {}
        
        for domain in self.domains:
            score = 0.0
            
            # Category preference scoring
            category_keywords = self.domain_keywords[domain]
            for category, count in features.get('category_preferences', {}).items():
                if any(keyword in category.lower() for keyword in category_keywords):
                    score += count * 0.1
            
            # Performance scoring
            if features['avg_score'] > 0.7:
                score += 0.2
            if features['avg_accuracy'] > 0.8:
                score += 0.15
            
            # Engagement scoring
            if features['emotional_engagement'] > 0.6:
                score += 0.2
            if features['completion_rate'] > 0.8:
                score += 0.15
            
            # Time investment scoring
            if features['total_play_time'] > 60:  # More than 1 hour
                score += 0.1
            
            # Initial interests matching
            if child_interests:
                for interest in child_interests:
                    if any(keyword in interest.lower() for keyword in category_keywords):
                        score += 0.2
            
            # Normalize score to 0-1 range
            scores[domain] = min(score, 1.0)
        
        return scores
    
    def ml_based_detection(self, features: Dict[str, Any]) -> Dict[str, float]:
        """ML-based passion detection using trained models"""
        scores = {}
        
        # Convert features to feature vector
        feature_vector = self._create_feature_vector(features)
        
        for domain in self.domains:
            if domain in self.models:
                try:
                    # Predict probability for this domain
                    prob = self.models[domain].predict_proba([feature_vector])[0]
                    scores[domain] = prob[1] if len(prob) > 1 else prob[0]  # Probability of positive class
                except Exception as e:
                    print(f"Error predicting for {domain}: {e}")
                    scores[domain] = 0.0
            else:
                scores[domain] = 0.0
        
        return scores
    
    def _create_feature_vector(self, features: Dict[str, Any]) -> List[float]:
        """Create a feature vector for ML models"""
        vector = [
            features.get('total_sessions', 0),
            features.get('completed_sessions', 0),
            features.get('completion_rate', 0),
            features.get('total_play_time', 0),
            features.get('avg_session_duration', 0),
            features.get('avg_score', 0),
            features.get('max_score', 0),
            features.get('avg_response_time', 0),
            features.get('avg_accuracy', 0),
            features.get('emotional_engagement', 0)
        ]
        
        # Add category preference features
        for domain in self.domains:
            category_count = 0
            for category, count in features.get('category_preferences', {}).items():
                if any(keyword in category.lower() for keyword in self.domain_keywords[domain]):
                    category_count += count
            vector.append(category_count)
        
        return vector
    
    def hybrid_detection(self, features: Dict[str, Any], child_interests: List[str] = None) -> Dict[str, float]:
        """Combine rule-based and ML-based detection"""
        rule_scores = self.rule_based_detection(features, child_interests)
        ml_scores = self.ml_based_detection(features)
        
        # Weighted combination (can be adjusted based on model performance)
        rule_weight = 0.6
        ml_weight = 0.4
        
        hybrid_scores = {}
        for domain in self.domains:
            rule_score = rule_scores.get(domain, 0.0)
            ml_score = ml_scores.get(domain, 0.0)
            hybrid_scores[domain] = rule_weight * rule_score + ml_weight * ml_score
        
        return hybrid_scores
    
    def determine_strength_level(self, confidence_score: float) -> str:
        """Determine strength level based on confidence score"""
        if confidence_score >= 0.8:
            return "very_high"
        elif confidence_score >= 0.6:
            return "high"
        elif confidence_score >= 0.4:
            return "medium"
        else:
            return "low"
    
    def generate_insights(self, child_id: int, domains: List[PassionDomain], features: Dict[str, Any]) -> List[PassionInsight]:
        """Generate insights based on detected passions"""
        insights = []
        
        # High confidence domain insight
        high_confidence_domains = [d for d in domains if d.confidence_score > 0.7]
        if high_confidence_domains:
            top_domain = max(high_confidence_domains, key=lambda x: x.confidence_score)
            insights.append(PassionInsight(
                child_id=child_id,
                insight_type="pattern",
                title=f"Strong {top_domain.domain} Interest Detected",
                description=f"Your child shows a strong interest in {top_domain.domain} activities with {top_domain.confidence_score:.1%} confidence.",
                importance_score=0.9,
                is_highlighted=True,
                notify_parent=True
            ))
        
        # Engagement insight
        if features.get('emotional_engagement', 0) > 0.7:
            insights.append(PassionInsight(
                child_id=child_id,
                insight_type="pattern",
                title="High Engagement Level",
                description="Your child shows high emotional engagement during activities, indicating strong interest in learning.",
                importance_score=0.7
            ))
        
        # Progress insight
        if features.get('completion_rate', 0) > 0.9:
            insights.append(PassionInsight(
                child_id=child_id,
                insight_type="milestone",
                title="Excellent Completion Rate",
                description="Your child completes 90%+ of activities, showing strong focus and determination.",
                importance_score=0.8
            ))
        
        return insights
    
    def analyze_child(self, child_id: int, db: Session) -> Dict[str, Any]:
        """Complete passion analysis for a child"""
        # Get child's sessions and games
        sessions = db.query(GameSession).filter(
            GameSession.child_id == child_id,
            GameSession.status == "completed"
        ).all()
        
        if not sessions:
            return {
                "child_id": child_id,
                "domains": [],
                "insights": [],
                "overall_confidence": 0.0,
                "recommended_next_activities": [],
                "development_trends": {},
                "last_updated": datetime.now()
            }
        
        # Get games
        game_ids = [s.game_id for s in sessions]
        games = db.query(Game).filter(Game.id.in_(game_ids)).all()
        
        # Extract features
        features = self.extract_features(sessions, games)
        
        # Get child's initial interests
        child = db.query(Child).filter(Child.id == child_id).first()
        child_interests = child.initial_interests if child else []
        
        # Detect passions
        passion_scores = self.hybrid_detection(features, child_interests)
        
        # Create passion domains
        domains = []
        for domain, score in passion_scores.items():
            if score > 0.3:  # Only create domains with reasonable confidence
                strength_level = self.determine_strength_level(score)
                
                domain_obj = PassionDomain(
                    child_id=child_id,
                    domain=domain,
                    confidence_score=score,
                    strength_level=strength_level,
                    detection_method="hybrid",
                    model_version=settings.MODEL_VERSION,
                    data_points_used=len(sessions),
                    supporting_evidence={
                        "total_sessions": features['total_sessions'],
                        "avg_score": features['avg_score'],
                        "emotional_engagement": features['emotional_engagement']
                    },
                    games_played=[g.name for g in games],
                    behavioral_patterns={
                        "completion_rate": features['completion_rate'],
                        "avg_response_time": features['avg_response_time'],
                        "category_preferences": features['category_preferences']
                    }
                )
                domains.append(domain_obj)
        
        # Generate insights
        insights = self.generate_insights(child_id, domains, features)
        
        # Calculate overall confidence
        overall_confidence = np.mean([d.confidence_score for d in domains]) if domains else 0.0
        
        # Generate recommendations
        recommended_activities = []
        for domain in domains:
            if domain.confidence_score > 0.6:
                recommended_activities.extend(domain.recommended_activities or [])
        
        return {
            "child_id": child_id,
            "domains": domains,
            "insights": insights,
            "overall_confidence": overall_confidence,
            "recommended_next_activities": recommended_activities[:5],  # Top 5 recommendations
            "development_trends": {d.domain: d.trend for d in domains},
            "last_updated": datetime.now()
        } 