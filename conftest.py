import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from constants import BASE_URL, EXISTING_USER
from locators import HeaderLocators, LoginLocators


@pytest.fixture
def driver():
    """Создает и закрывает браузер"""
    driver = webdriver.Chrome()
    driver.get(BASE_URL)
    WebDriverWait(driver, 3)
    yield driver
    driver.quit()


@pytest.fixture
def auth_driver(driver):
    """
    Предусловие: авторизованный пользователь.
    Возвращает драйвер с уже выполненным входом.
    """
    from helpers import LoginSteps
    
    # Открываем модалку
    login_btn = WebDriverWait(driver, 5).until(
        expected_conditions.element_to_be_clickable(LoginLocators.LOGIN_BUTTON)
    )
    login_btn.click()
    
    # Выполняем вход
    LoginSteps.login(driver, EXISTING_USER["email"], EXISTING_USER["password"])
    
    # Ждем, что авторизация прошла (это предусловие, а не проверка)
    WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located(HeaderLocators.PROFILE_AVATAR)
    )
    
    yield driver