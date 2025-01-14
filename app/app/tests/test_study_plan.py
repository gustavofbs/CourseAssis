import pytest
from app.patterns.study_plan_template import CourseraStudyPlanGenerator
from app.patterns.recommendation_strategy import RecommendationStrategy

def test_study_plan_generation():
    """Test the generation of a study plan"""
    generator = CourseraStudyPlanGenerator()
    plan = generator.create_study_plan(
        course_data={
            "course_name": "Python Programming",
            "course_description": "Learn Python from basics to advanced",
            "description": "Learn Python from basics to advanced"
        },
        user_preferences={
            "weekly_hours": 10,
            "start_date": "2025-01-20",
            "end_date": "2025-03-20",
            "fundamentals_percent": 30,
            "development_percent": 40,
            "project_percent": 30
        }
    )
    
    assert isinstance(plan, dict)
    assert "weekly_breakdown" in plan
    assert len(plan["weekly_breakdown"]) > 0

def test_recommendation_strategy():
    """Test the recommendation system"""
    strategy = RecommendationStrategy()
    recommendations = strategy.generate_recommendations(
        user_data={
            "name": "Test User",
            "interests": ["Python", "Web Development"],
            "experience_level": "intermediate"
        }
    )
    
    assert isinstance(recommendations, dict)
    assert "content" in recommendations
    assert "type" in recommendations
    assert recommendations["type"] == "course_recommendation"

def test_invalid_study_plan_parameters():
    """Test validation of study plan parameters"""
    generator = CourseraStudyPlanGenerator()
    
    with pytest.raises(ValueError):
        generator.create_study_plan(
            course_data={
                "course_name": "",
                "course_description": "Test description"
            },
            user_preferences={
                "weekly_hours": -1,
                "start_date": "2025-01-20",
                "end_date": "2025-01-19",
                "fundamentals_percent": 30,
                "development_percent": 40,
                "project_percent": 40
            }
        )
