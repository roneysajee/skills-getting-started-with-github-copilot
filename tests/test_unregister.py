"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
"""


def test_unregister_existing_participant_success(client):
    """
    Test successful unregistration of an existing participant
    
    Arrange: Use an email already registered in an activity
    Act: Send DELETE request to unregister endpoint
    Assert: Verify success response and participant is removed
    """
    # Arrange
    email = "michael@mergington.edu"  # Exists in Chess Club
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    
    # Verify participant was actually removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_activity_not_found(client):
    """
    Test unregister fails when activity doesn't exist
    
    Arrange: Prepare valid email but invalid activity
    Act: Send DELETE request with non-existent activity
    Assert: Verify 404 error response
    """
    # Arrange
    email = "student@mergington.edu"
    activity = "Non-Existent Activity"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_not_signed_up(client):
    """
    Test unregister fails when student is not registered
    
    Arrange: Use an email not registered in the activity
    Act: Send DELETE request to unregister
    Assert: Verify 400 error response
    """
    # Arrange
    email = "notregistered@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_preserves_other_participants(client):
    """
    Test that unregister only removes the target participant
    
    Arrange: Get participants, unregister one
    Act: Send DELETE request for one participant
    Assert: Verify other participants remain
    """
    # Arrange
    email_to_remove = "michael@mergington.edu"
    email_to_keep = "daniel@mergington.edu"
    activity = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email_to_remove}
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify correct participant removed
    activities = client.get("/activities").json()
    assert email_to_remove not in activities[activity]["participants"]
    
    # Verify other participants remain
    assert email_to_keep in activities[activity]["participants"]


def test_unregister_decreases_participant_count(client):
    """
    Test that unregister decreases the participant count
    
    Arrange: Get initial participant count
    Act: Send DELETE request to unregister
    Assert: Verify participant count decreased by 1
    """
    # Arrange
    email = "emma@mergington.edu"
    activity = "Programming Class"
    
    initial = client.get("/activities").json()
    initial_count = len(initial[activity]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    
    updated = client.get("/activities").json()
    updated_count = len(updated[activity]["participants"])
    
    assert updated_count == initial_count - 1


def test_unregister_returns_correct_message_format(client):
    """
    Test that unregister returns properly formatted success message
    
    Arrange: Prepare email in an activity
    Act: Send DELETE request to unregister
    Assert: Verify message contains email and activity name
    """
    # Arrange
    email = "lucas@mergington.edu"  # In Science Olympiad
    activity = "Science Olympiad"
    
    # Act
    response = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    message = data["message"]
    assert email in message
    assert activity in message
    assert "Unregistered" in message or "unregistered" in message.lower()


def test_unregister_can_signup_again(client):
    """
    Test that after unregistering, a participant can sign up again
    
    Arrange: Unregister a participant
    Act: Sign them up again
    Assert: Verify they are successfully registered again
    """
    # Arrange
    email = "ava@mergington.edu"
    activity = "Drama Club"
    
    # Act - First unregister
    response1 = client.delete(
        f"/activities/{activity}/unregister",
        params={"email": email}
    )
    assert response1.status_code == 200
    
    # Verify they were removed
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
    
    # Act - Then sign up again
    response2 = client.post(
        f"/activities/{activity}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response2.status_code == 200
    
    # Verify they are back
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]
