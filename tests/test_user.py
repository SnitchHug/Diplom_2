import allure
import pytest

from api.user import User
from helpers import generation
from helpers.message import Message


@allure.feature("Создание пользователя")
class TestCreateCourier:
    @allure.story("Успешное создание уникального пользователя")
    @allure.title("Тест на успешное создание пользователя со всеми полями")
    def test_create_user_successful(self):
        user_data = generation.generate_user_data()
        response = User.register_new_user(user_data)
        token = response.json().get('accessToken')

        assert (response.status_code == 200 and
                response.json()['success'] is True and
                'user' in response.json() and
                'accessToken' in response.json())

        User.delete_new_user(token)

    @allure.story("Ошибка при повторном создании пользователя")
    @allure.title("Тест на создание пользователя с уже существующим логином")
    def test_create_user_repeat_login_error(self, create_and_delete_user):
        user_data = create_and_delete_user
        response = User.register_new_user(user_data)

        assert (response.status_code == 403 and
                response.json()['success'] is False and
                response.json().get('message') == Message.USER_ALREADY_EXISTS)

    @allure.story("Ошибка при создании учетной записи курьера без обязательных полей")
    @allure.title("Тест на создание учетной записи курьера без обязательного поля")
    @pytest.mark.parametrize("user_data", [
        (generation.generate_user_data(include_first_name=False)),
        (generation.generate_user_data(include_email=False)),
        (generation.generate_user_data(include_password=False)),
    ])
    def test_create_user_no_required_field_error(self, user_data):
        response = User.register_new_user(user_data)

        assert (response.status_code == 403 and
                response.json()['success'] is False and
                response.json().get('message') == Message.EMAIL_PASSWORD_NAME_REQUIRED)


@allure.feature("Авторизация пользователя")
class TestLoginUser:
    @allure.story("Успешная авторизация пользователя")
    @allure.title("Тест на авторизацию пользователя при передаче всех обязательных полей")
    def test_login_user_successful(self, create_and_delete_user):
        user_data = create_and_delete_user
        response = User.login_user(user_data.get('email', ''), user_data.get('password', ''))
        token = response.json().get('accessToken')
        assert (response.status_code == 200 and
                response.json()['success'] is True and
                'user' in response.json() and
                token)

    @allure.story("Ошибка если неправильно указать логин или пароль")
    @allure.title("Тест на авторизацию с заменой значения у обязательного поля")
    def test_login_user_invalid_value_error(self):
        response = User.login_user(generation.generate_email(), generation.generate_password())

        assert (response.status_code == 401 and
                response.json()['success'] is False and
                response.json().get('message') == Message.EMAIL_PASSWORD_INCORRECT)


@allure.feature("Изменения данных пользователя")
class TestChangeUserData:
    @allure.story("Успешное изменение данных пользователя")
    @allure.title("Тест на изменение данных пользователя с авторизацией")
    @pytest.mark.parametrize("value", ["email", "name"])
    def test_change_user_data_successful(self, create_and_delete_user, value):
        user_data = create_and_delete_user
        email = user_data.get('email', '')
        password = user_data.get('password', '')
        response = User.login_user(user_data.get('email', email), user_data.get('password', password))
        token = response.json().get('accessToken')

        updated_data = user_data.copy()
        if value == "email":
            updated_data['email'] = "newemail123@mail.com"
        elif value == "name":
            updated_data['name'] = "NewUsername123"

        change_response = User.change_user_data(token, updated_data)
        assert (change_response.status_code == 200 and
                change_response.json()['success'] is True and
                'user' in change_response.json())

    @allure.story("Ошибка при изменении данных пользователя")
    @allure.title("Тест на изменение данных пользователя без авторизации")
    @pytest.mark.parametrize("value", ["email", "name"])
    def test_change_user_data_without_authorization_error(self, create_and_delete_user, value):
        user_data = create_and_delete_user
        email = user_data.get('email', '')
        password = user_data.get('password', '')
        User.login_user(user_data.get('email', email), user_data.get('password', password))
        token = None

        updated_data = user_data.copy()
        if value == "email":
            updated_data['email'] = "newemail123@mail.com"
        elif value == "name":
            updated_data['name'] = "NewUsername123"

        change_response = User.change_user_data(token, updated_data)
        assert (change_response.status_code == 401 and
                change_response.json()['success'] is False and
                change_response.json().get('message') == Message.WITHOUT_AUTHORIZATION)
