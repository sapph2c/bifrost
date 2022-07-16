import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/")))

from src.c2.app import create_app
from src.c2.models import Agent, Command, User


@pytest.fixture(scope="module")
def new_user():
    user = User("testuser@gmail.com", "testuser", "1234")
    return user


@pytest.fixture(scope="module")
def new_agent():
    agent = Agent("testhost", "testos", "testagent", "127.0.0.1", 1)
    return agent


@pytest.fixture(scope="module")
def new_command():
    command = Command("1")
    return command


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!
