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
from app.core.config import settings

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