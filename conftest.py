import pytest
import requests

from api.user import User
from helpers import generation, url


@pytest.fixture
def create_and_delete_user():
    user_data = generation.generate_user_data()
    response = requests.post(url.CREATE_USER, json=user_data)
    user_token = response.json().get('accessToken')
    yield user_data

    delete_headers = {
        'Accept': 'application/json',
        'Authorization': user_token
    }
    requests.delete(url.DELETE_USER, headers=delete_headers)


@pytest.fixture
def login_in(create_and_delete_user):
    user_data = create_and_delete_user
    email = user_data.get('email', '')
    password = user_data.get('password', '')
    response = User.login_user(email, password)
    return response
