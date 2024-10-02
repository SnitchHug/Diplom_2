import allure
import pytest
import requests

from helpers import url


class User:
    @staticmethod
    @allure.step("Создание нового пользователя")
    def register_new_user(user_data):
        response = requests.post(url.CREATE_USER, json=user_data)
        return response

    @staticmethod
    @allure.step("Удаление нового пользователя")
    def delete_new_user(token):
        delete_headers = {
            'Accept': 'application/json',
            'Authorization': f'{token}'
        }
        delete_response = requests.delete(url.DELETE_USER, headers=delete_headers)

        if delete_response.status_code != 202:
            pytest.fail(f"Ошибка при удалении пользователя: {delete_response.status_code} - {delete_response.text}")

    @staticmethod
    @allure.step("Логин пользователя")
    def login_user(login, password):
        response = requests.post(url.LOGIN_USER, json={'email': login, 'password': password})
        return response

    @staticmethod
    @allure.step("Изменить данные пользователя")
    def change_user_data(token, updated_data):
        change_headers = {
            'Accept': 'application/json',
            'Authorization': f'{token}'
        }
        change_response = requests.patch(url.CHANGE_USER_DATA, headers=change_headers, json=updated_data)
        return change_response
