"""
Tests for the root endpoint (GET /).
"""


def test_root_redirect(client):
    """
    Test that the root endpoint redirects to /static/index.html
    
    Arrange: No setup needed
    Act: Send GET request to /
    Assert: Verify redirect status code and location
    """
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code in [307, 308]  # Temporary or permanent redirect
    assert "/static/index.html" in response.headers.get("location", "")


def test_root_redirect_follows(client):
    """
    Test that following the redirect from / leads to index.html
    
    Arrange: No setup needed
    Act: Send GET request to / with follow_redirects=True
    Assert: Verify final response is successful
    """
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
