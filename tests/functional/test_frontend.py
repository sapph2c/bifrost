SUCCESS = 200
REDIRECT = 302


def test_signup(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/signup' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/signup")
    assert response.status_code == SUCCESS


def test_home_unauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == REDIRECT


def test_config_unauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/config' page is requested (GET) by a non-authenticated user
    THEN check that the user is redirected to login
    """
    response = test_client.get("/config")
    assert response.status_code == REDIRECT


def test_agent_unauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/agent<id>' page is requested (GET) by a non-authenticated user
    THEN check that the user is redirected to login
    """
    response = test_client.get("/agent1")
    assert response.status_code == REDIRECT


def test_logout_unauth(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/logout' page is requested (GET) by a non-authenticated usser
    THEN check that the user is redirected to login
    """
    response = test_client.get("/logout")
    assert response.status_code == REDIRECT
