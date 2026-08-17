"""
Tests for the GET /activities endpoint.
"""


def test_get_activities_returns_all(client):
    """
    Test that GET /activities returns all activities
    
    Arrange: No setup needed
    Act: Send GET request to /activities
    Assert: Verify response contains all 9 activities
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 9
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Debate Team" in data


def test_get_activities_correct_structure(client):
    """
    Test that each activity has the correct structure
    
    Arrange: No setup needed
    Act: Send GET request to /activities
    Assert: Verify each activity has required fields
    """
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert - Check first activity has all required fields
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club


def test_get_activities_correct_participant_count(client):
    """
    Test that activities show correct initial participant counts
    
    Arrange: No setup needed
    Act: Send GET request to /activities
    Assert: Verify participants list matches expected values
    """
    # Act
    response = client.get("/activities")
    data = response.json()
    
    # Assert
    assert len(data["Chess Club"]["participants"]) == 2
    assert "michael@mergington.edu" in data["Chess Club"]["participants"]
    assert "daniel@mergington.edu" in data["Chess Club"]["participants"]


def test_get_activities_returns_json(client):
    """
    Test that GET /activities returns valid JSON
    
    Arrange: No setup needed
    Act: Send GET request to /activities
    Assert: Verify response is JSON and can be parsed
    """
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.headers["content-type"].startswith("application/json")
    data = response.json()
    assert isinstance(data, dict)
