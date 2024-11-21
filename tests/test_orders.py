import allure

from api.orders import Order
from api.user import User
from helpers.generation import generate_body_order
from helpers.message import Message


@allure.feature("Создание заказа")
class TestCreateOrder:
    @allure.story("Успешное создание заказа с авторизацией и с ингридиентами")
    @allure.title("Тест на создание заказа с авторизацией и с ингридиентами")
    def test_create_order_successful(self, login_in):
        token = login_in.json().get('accessToken')
        body_order = generate_body_order()

        order_response = Order.create_order(token, body_order)
        assert (order_response.status_code == 200 and
                order_response.json()['success'] is True and
                'order' in order_response.json())

    @allure.story("Успешное создание заказа без авторизации")
    @allure.title("Тест на создание заказа без авторизации")
    def test_create_order_without_authorization_successful(self, create_and_delete_user):
        user_data = create_and_delete_user
        email = user_data.get('email', '')
        password = user_data.get('password', '')
        User.login_user(user_data.get('email', email), user_data.get('password', password))
        token = None
        body_order = generate_body_order()

        order_response = Order.create_order(token, body_order)
        assert (order_response.status_code == 200 and
                order_response.json()['success'] is True and
                'order' in order_response.json())

    @allure.story("Ошибка при создании заказа с авторизацией без ингридиентов")
    @allure.title("Тест на создание заказа с авторизацией без ингридиентов")
    def test_create_order_without_ingredient_error(self, login_in):
        token = login_in.json().get('accessToken')
        body_order = None

        order_response = Order.create_order(token, body_order)
        assert (order_response.status_code == 400 and
                order_response.json().get('message') == Message.WITHOUT_INGREDIENT and
                order_response.json()['success'] is False)

    @allure.story("Ошибка при создании заказа с авторизацией с неверным хешем ингредиентов")
    @allure.title("Тест на создание заказа с авторизацией с неверным хешем ингредиентов")
    def test_create_order_incorrect_ingredient_error(self, login_in):
        token = login_in.json().get('accessToken')
        body_order = {"ingredients": ["61c0c5a71d1f82001bdaaa73232321", "61c0c5a71d1f82001bdaaa6c233232"]}

        order_response = Order.create_order(token, body_order)
        assert order_response.status_code == 500


@allure.feature("Получение заказов конкретного пользователя")
class TestGetOrder:
    @allure.story("Успешное получение заказов конкретного пользователя с авторизацией")
    @allure.title("Тест на получение заказов конкретного пользователя с авторизацией")
    def test_get_order_successful(self, login_in):
        token = login_in.json().get('accessToken')
        body_order = generate_body_order()
        Order.create_order(token, body_order)

        get_order_response = Order.get_order(token)
        assert (get_order_response.status_code == 200 and
                get_order_response.json()['success'] is True and
                'orders' in get_order_response.json())

    @allure.story("Ошибка при попытке получения заказов без авторизации")
    @allure.title("Тест на получение заказов без авторизации")
    def test_get_order_without_authorization_error(self, login_in):
        token = login_in.json().get('accessToken')
        body_order = generate_body_order()
        Order.create_order(token, body_order)
        token = None

        get_order_response = Order.get_order(token)
        assert (get_order_response.status_code == 401 and
                get_order_response.json()['success'] is False and
                get_order_response.json().get('message') == Message.WITHOUT_AUTHORIZATION)
