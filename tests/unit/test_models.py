def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    assert new_user.email == "testuser@gmail.com"
    assert new_user.username == "testuser"
    assert new_user.password != "1234"


def test_new_agent(new_agent):
    """
    GIVE a Agent model
    WHEN a new Agent is created
    THEN check the hostname, os, username, ip, and sleep_time are defined correctly
    """
    assert new_agent.hostname == "testhost"
    assert new_agent.os == "testos"
    assert new_agent.username == "testagent"
    assert new_agent.ip == "127.0.0.1"
    assert new_agent.sleep_time == 1


def test_new_command(new_command):
    """
    GIVEN a Command model
    WHEN a new Command is created
    THEN check the agent_id, command, output, retrieved, and displayed are defined correctly
    """
    assert new_command.agent_id == "1"
    assert new_command.command == None
    assert new_command.output == None
    assert new_command.retrieved == False
    assert new_command.displayed == False
