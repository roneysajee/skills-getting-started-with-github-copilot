"""
Shared test fixtures and configuration for the Mergington High School API tests.
"""
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities(sample_activities):
    """
    Fixture to reset activities to initial state before each test.
    This ensures test isolation by preventing cross-test contamination.
    
    autouse=True means this fixture runs automatically before every test.
    """
    # Reset the activities dict to initial state
    app_module.app.dependency_overrides.clear()
    app_module.activities.clear()
    app_module.activities.update(sample_activities)
    yield
    # Cleanup after test (optional, but good practice)
    app_module.activities.clear()


@pytest.fixture
def client():
    """
    Fixture providing a TestClient for the FastAPI app.
    This client can be used to make HTTP requests to the app in tests.
    """
    return TestClient(app_module.app)


@pytest.fixture
def sample_activities():
    """
    Fixture providing a copy of sample activities data for test isolation.
    Each test gets fresh data without cross-test contamination.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Practice teamwork and compete in soccer matches against other schools",
            "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["alex@mergington.edu", "miguel@mergington.edu"]
        },
        "Basketball Club": {
            "description": "Improve shooting, dribbling, and defensive skills in a competitive setting",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Explore acting, stage performance, and dramatic storytelling",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
        },
        "Art Workshop": {
            "description": "Create paintings, sketches, and mixed-media projects in a collaborative studio",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Solve challenging science problems and compete in STEM events",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["lucas@mergington.edu", "henry@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop public speaking skills and learn formal argumentation techniques",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
        }
    }
