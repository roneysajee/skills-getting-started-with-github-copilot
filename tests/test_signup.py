"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""


def test_signup_new_participant_success(client):
    """
    Test successful signup of a new participant to an activity
    
    Arrange: Prepare email and activity name
    Act: Send POST request to signup endpoint
    Assert: Verify success response and participant is added
    """
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    
    # Verify participant was actually added
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_activity_not_found(client):
    """
    Test signup fails when activity doesn't exist
    
    Arrange: Prepare valid email but invalid activity
    Act: Send POST request with non-existent activity
    Assert: Verify 404 error response
    """
    # Arrange
    email = "student@mergington.edu"
    activity = "Non-Existent Activity"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_already_signed_up(client):
    """
    Test signup fails when student is already registered
    
    Arrange: Use an email already registered in Chess Club
    Act: Send POST request to signup with duplicate email
    Assert: Verify 400 error response
    """
    # Arrange
    email = "michael@mergington.edu"  # Already in Chess Club
    activity = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_preserves_existing_participants(client):
    """
    Test that signup preserves existing participants in the activity
    
    Arrange: Get current participants, add new one
    Act: Send POST request to signup
    Assert: Verify all previous participants are still there
    """
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Programming Class"
    
    # Get initial participants
    initial = client.get("/activities").json()
    initial_participants = initial[activity]["participants"].copy()
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify all original participants still exist
    updated = client.get("/activities").json()
    updated_participants = updated[activity]["participants"]
    
    for original_email in initial_participants:
        assert original_email in updated_participants
    
    # And new one is added
    assert email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_special_characters_in_email(client):
    """
    Test signup works with special characters in email
    
    Arrange: Prepare email with special characters (URL encoded)
    Act: Send POST request with special character email
    Assert: Verify successful signup
    """
    # Arrange
    email = "student+tag@mergington.edu"
    activity = "Drama Club"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_returns_correct_message_format(client):
    """
    Test that signup returns properly formatted success message
    
    Arrange: Prepare email and activity
    Act: Send POST request to signup
    Assert: Verify message contains email and activity name
    """
    # Arrange
    email = "testuser@mergington.edu"
    activity = "Science Olympiad"
    
    # Act
    response = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    message = data["message"]
    assert email in message
    assert activity in message
