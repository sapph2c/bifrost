import requests


BASE_URL = "http://127.0.0.1:5000/api/1.1"

ERROR = "Bad Request"


def test_register_agent_insufficient_params():
    response = requests.post(f"{BASE_URL}/register_agent").text
    assert ERROR in response


def test_get_command_agent_not_exist():
    params = { 'agent_id' : '99999'}
    response = requests.post(f"{BASE_URL}/get_command", params=params).text
    assert ERROR in response
