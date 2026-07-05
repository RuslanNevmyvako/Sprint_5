import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from locators import LoginLocators, HeaderLocators
from helpers import LoginSteps
from constants import EXISTING_USER


class TestLogin:
    
    def test_login_success(self, driver):
        """Успешный вход в систему"""
        # ШАГИ
        LoginSteps.open_login_modal(driver)
        LoginSteps.login(driver, EXISTING_USER["email"], EXISTING_USER["password"])
        
        # ПРОВЕРКИ
        avatar = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located(HeaderLocators.PROFILE_AVATAR)
        )
        assert avatar.is_displayed(), "Аватар не отображается"
        
        user_name = driver.find_element(*HeaderLocators.USER_NAME)
        assert user_name.is_displayed(), "Имя пользователя не отображается"
        assert user_name.text == "User.", f"Ожидалось 'User.', получено '{user_name.text}'"
    
    def test_logout(self, auth_driver):
        """Выход из системы"""
        driver = auth_driver
        
        # ШАГИ
        LoginSteps.logout(driver)
        
        WebDriverWait(driver, 5).until(expected_conditions.invisibility_of_element_located(HeaderLocators.PROFILE_AVATAR))

        # ПРОВЕРКИ
        avatars = driver.find_elements(*HeaderLocators.PROFILE_AVATAR)
        assert len(avatars) == 0, "Аватар всё еще отображается"
        
        user_names = driver.find_elements(*HeaderLocators.USER_NAME)
        assert len(user_names) == 0, "Имя пользователя всё еще отображается"
        
        login_btn = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(LoginLocators.LOGIN_BUTTON)
        )
        assert login_btn.is_displayed(), "Кнопка 'Вход и регистрация' не отображается"