#!/usr/bin/env python3
"""
Seed the database with sample questions for talent detection
"""

from app.core.database import SessionLocal
from app.models.question import Question

def seed_questions():
    """Seed the database with sample questions"""
    print("Seeding sample questions...")
    
    try:
        db = SessionLocal()
        
        # Check if questions already exist
        existing_questions = db.query(Question).count()
        if existing_questions > 0:
            print("✅ Sample questions already exist")
            db.close()
            return True
        
        # Sample questions for different talent domains
        sample_questions = [
            # Artistic Creativity Questions
            Question(
                question_text="When you see a blank piece of paper, what do you want to do with it?",
                question_type="multiple_choice",
                category="art",
                talent_domain="artistic_creativity",
                options=["Draw pictures", "Write a story", "Make origami", "Leave it blank"],
                min_age=3,
                max_age=12,
                difficulty_level="easy",
                scoring_weights={"Draw pictures": 0.9, "Make origami": 0.8, "Write a story": 0.6, "Leave it blank": 0.2},
                expected_duration=30
            ),
            Question(
                question_text="What colors do you like to use when drawing?",
                question_type="multiple_choice",
                category="art",
                talent_domain="artistic_creativity",
                options=["Bright colors (red, yellow, blue)", "Soft colors (pink, purple, green)", "Dark colors (black, brown, gray)", "All colors mixed together"],
                min_age=3,
                max_age=8,
                difficulty_level="easy",
                scoring_weights={"Bright colors (red, yellow, blue)": 0.8, "All colors mixed together": 0.9, "Soft colors (pink, purple, green)": 0.7, "Dark colors (black, brown, gray)": 0.4},
                expected_duration=25
            ),
            Question(
                question_text="If you could create anything with your imagination, what would it be?",
                question_type="open_ended",
                category="art",
                talent_domain="artistic_creativity",
                min_age=5,
                max_age=12,
                difficulty_level="medium",
                expected_duration=45
            ),
            
            # Musical Rhythm Questions
            Question(
                question_text="When you hear music, what do you want to do?",
                question_type="multiple_choice",
                category="music",
                talent_domain="musical_rhythm",
                options=["Dance and move", "Sing along", "Listen quietly", "Cover your ears"],
                min_age=3,
                max_age=10,
                difficulty_level="easy",
                scoring_weights={"Dance and move": 0.9, "Sing along": 0.8, "Listen quietly": 0.6, "Cover your ears": 0.1},
                expected_duration=25
            ),
            Question(
                question_text="Can you tap your foot to the beat of a song?",
                question_type="rating",
                category="music",
                talent_domain="musical_rhythm",
                min_age=4,
                max_age=12,
                difficulty_level="easy",
                expected_duration=20
            ),
            Question(
                question_text="What kind of sounds do you like to make?",
                question_type="multiple_choice",
                category="music",
                talent_domain="musical_rhythm",
                options=["Singing", "Drumming on things", "Whistling", "Making animal sounds"],
                min_age=3,
                max_age=8,
                difficulty_level="easy",
                scoring_weights={"Singing": 0.8, "Drumming on things": 0.9, "Whistling": 0.7, "Making animal sounds": 0.5},
                expected_duration=25
            ),
            
            # Logical Mathematics Questions
            Question(
                question_text="Do you like to solve puzzles?",
                question_type="rating",
                category="logic",
                talent_domain="logical_mathematics",
                min_age=4,
                max_age=12,
                difficulty_level="easy",
                expected_duration=20
            ),
            Question(
                question_text="When you see numbers, what do you think about?",
                question_type="multiple_choice",
                category="logic",
                talent_domain="logical_mathematics",
                options=["Counting them", "Adding them together", "Finding patterns", "Nothing special"],
                min_age=5,
                max_age=12,
                difficulty_level="medium",
                scoring_weights={"Finding patterns": 0.9, "Adding them together": 0.8, "Counting them": 0.7, "Nothing special": 0.3},
                expected_duration=30
            ),
            Question(
                question_text="If you have 3 apples and get 2 more, how many do you have?",
                question_type="multiple_choice",
                category="logic",
                talent_domain="logical_mathematics",
                options=["3", "4", "5", "6"],
                min_age=4,
                max_age=8,
                difficulty_level="easy",
                scoring_weights={"5": 1.0, "4": 0.8, "6": 0.6, "3": 0.2},
                expected_duration=20
            ),
            
            # Sports & Movement Questions
            Question(
                question_text="What do you like to do when you're outside?",
                question_type="multiple_choice",
                category="sports",
                talent_domain="sports_movement",
                options=["Run and play", "Climb trees", "Play sports", "Sit and watch"],
                min_age=3,
                max_age=10,
                difficulty_level="easy",
                scoring_weights={"Run and play": 0.8, "Climb trees": 0.9, "Play sports": 0.9, "Sit and watch": 0.3},
                expected_duration=25
            ),
            Question(
                question_text="Can you balance on one foot?",
                question_type="rating",
                category="sports",
                talent_domain="sports_movement",
                min_age=4,
                max_age=12,
                difficulty_level="easy",
                expected_duration=20
            ),
            Question(
                question_text="What's your favorite way to move your body?",
                question_type="multiple_choice",
                category="sports",
                talent_domain="sports_movement",
                options=["Dancing", "Running", "Jumping", "Walking slowly"],
                min_age=3,
                max_age=8,
                difficulty_level="easy",
                scoring_weights={"Dancing": 0.8, "Running": 0.9, "Jumping": 0.9, "Walking slowly": 0.4},
                expected_duration=25
            ),
            
            # Language & Communication Questions
            Question(
                question_text="Do you like to tell stories?",
                question_type="rating",
                category="language",
                talent_domain="language_communication",
                min_age=4,
                max_age=12,
                difficulty_level="easy",
                expected_duration=20
            ),
            Question(
                question_text="What do you like to read about?",
                question_type="multiple_choice",
                category="language",
                talent_domain="language_communication",
                options=["Adventure stories", "Science facts", "Animal books", "I don't like reading"],
                min_age=5,
                max_age=12,
                difficulty_level="medium",
                scoring_weights={"Adventure stories": 0.8, "Science facts": 0.7, "Animal books": 0.7, "I don't like reading": 0.2},
                expected_duration=30
            ),
            Question(
                question_text="If you could talk to anyone, who would it be?",
                question_type="open_ended",
                category="language",
                talent_domain="language_communication",
                min_age=5,
                max_age=12,
                difficulty_level="medium",
                expected_duration=45
            ),
            
            # Social Leadership Questions
            Question(
                question_text="Do you like to help other children?",
                question_type="rating",
                category="social",
                talent_domain="social_leadership",
                min_age=4,
                max_age=12,
                difficulty_level="easy",
                expected_duration=20
            ),
            Question(
                question_text="When playing with friends, what role do you usually take?",
                question_type="multiple_choice",
                category="social",
                talent_domain="social_leadership",
                options=["Leader of the group", "Helper and supporter", "Quiet observer", "I prefer to play alone"],
                min_age=5,
                max_age=12,
                difficulty_level="medium",
                scoring_weights={"Leader of the group": 0.9, "Helper and supporter": 0.8, "Quiet observer": 0.5, "I prefer to play alone": 0.3},
                expected_duration=30
            ),
            Question(
                question_text="How do you feel when you work with a team?",
                question_type="multiple_choice",
                category="social",
                talent_domain="social_leadership",
                options=["Excited and happy", "Comfortable", "A little nervous", "I don't like teams"],
                min_age=6,
                max_age=12,
                difficulty_level="medium",
                scoring_weights={"Excited and happy": 0.9, "Comfortable": 0.7, "A little nervous": 0.5, "I don't like teams": 0.2},
                expected_duration=30
            ),
            
            # Scientific Discovery Questions
            Question(
                question_text="Do you like to ask 'why' questions?",
                question_type="rating",
                category="science",
                talent_domain="scientific_discovery",
                min_age=4,
                max_age=12,
                difficulty_level="easy",
                expected_duration=20
            ),
            Question(
                question_text="What happens when you mix water and oil?",
                question_type="multiple_choice",
                category="science",
                talent_domain="scientific_discovery",
                options=["They mix together", "They separate", "They turn into a solid", "I don't know"],
                min_age=6,
                max_age=12,
                difficulty_level="medium",
                scoring_weights={"They separate": 0.9, "I don't know": 0.5, "They mix together": 0.3, "They turn into a solid": 0.2},
                expected_duration=30
            ),
            Question(
                question_text="What would you like to discover or invent?",
                question_type="open_ended",
                category="science",
                talent_domain="scientific_discovery",
                min_age=6,
                max_age=12,
                difficulty_level="hard",
                expected_duration=60
            ),
            
            # Technology & Innovation Questions
            Question(
                question_text="Do you like to figure out how things work?",
                question_type="rating",
                category="technology",
                talent_domain="technology_innovation",
                min_age=4,
                max_age=12,
                difficulty_level="easy",
                expected_duration=20
            ),
            Question(
                question_text="What would you do with a computer?",
                question_type="multiple_choice",
                category="technology",
                talent_domain="technology_innovation",
                options=["Play games", "Learn to code", "Draw pictures", "Watch videos"],
                min_age=5,
                max_age=12,
                difficulty_level="medium",
                scoring_weights={"Learn to code": 0.9, "Draw pictures": 0.7, "Play games": 0.6, "Watch videos": 0.4},
                expected_duration=30
            ),
            Question(
                question_text="If you could build anything, what would it be?",
                question_type="open_ended",
                category="technology",
                talent_domain="technology_innovation",
                min_age=5,
                max_age=12,
                difficulty_level="medium",
                expected_duration=45
            ),
            
            # Scenario-based questions for older children
            Question(
                question_text="Imagine you're stranded on an island. What would you do first?",
                question_type="multiple_choice",
                category="problem_solving",
                talent_domain="logical_mathematics",
                options=["Build a shelter", "Look for food", "Make a signal fire", "Explore the island"],
                min_age=8,
                max_age=12,
                difficulty_level="hard",
                scoring_weights={"Build a shelter": 0.8, "Make a signal fire": 0.9, "Look for food": 0.7, "Explore the island": 0.6},
                expected_duration=40
            ),
            Question(
                question_text="If you could solve one problem in the world, what would it be?",
                question_type="open_ended",
                category="social",
                talent_domain="social_leadership",
                min_age=8,
                max_age=12,
                difficulty_level="hard",
                expected_duration=60
            )
        ]
        
        # Add questions to database
        for question in sample_questions:
            db.add(question)
        
        db.commit()
        print(f"✅ Added {len(sample_questions)} sample questions")
        
        # Print summary
        print("\n📊 Question Summary:")
        categories = {}
        domains = {}
        for question in sample_questions:
            categories[question.category] = categories.get(question.category, 0) + 1
            domains[question.talent_domain] = domains.get(question.talent_domain, 0) + 1
        
        print("Categories:")
        for category, count in categories.items():
            print(f"  - {category}: {count} questions")
        
        print("\nTalent Domains:")
        for domain, count in domains.items():
            print(f"  - {domain}: {count} questions")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error seeding questions: {e}")
        db.close()
        return False

if __name__ == "__main__":
    seed_questions() 