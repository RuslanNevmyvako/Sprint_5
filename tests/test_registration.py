from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from locators import LoginLocators, RegistrationFormLocators, HeaderLocators
from helpers import RegistrationSteps
from constants import TEST_USER, EXISTING_USER


class TestRegistration:
    
    def test_successful_registration(self, driver):
        """Успешная регистрация нового пользователя"""
        # ШАГИ
        RegistrationSteps.open_login_modal(driver)
        RegistrationSteps.go_to_registration(driver)
        email = RegistrationSteps.generate_unique_email()
        RegistrationSteps.fill_registration_form(driver, email, TEST_USER["password"])
        
        # ПРОВЕРКИ
        avatar = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located(HeaderLocators.PROFILE_AVATAR)
        )
        assert avatar.is_displayed(), "Аватар не отображается"
        
        user_name = driver.find_element(*HeaderLocators.USER_NAME)
        assert user_name.is_displayed(), "Имя пользователя не отображается"
        assert user_name.text == "User.", f"Ожидалось 'User.', получено '{user_name.text}'"
    
    def test_registration_invalid_email(self, driver):
        """Регистрация с некорректным email"""
        # ШАГИ
        RegistrationSteps.open_login_modal(driver)
        RegistrationSteps.go_to_registration(driver)
        driver.find_element(*RegistrationFormLocators.EMAIL_INPUT).send_keys("invalid-email")
        driver.find_element(*LoginLocators.REGISTER_SUBMIT).click()
        RegistrationSteps.wait_for_error(driver)
        
        # ПРОВЕРКИ
        for field in ["email", "password", "submitPassword"]:
            parent = driver.find_element(*LoginLocators.error_field(field))
            error_class = parent.get_attribute("class")
            assert "input_inputError" in error_class, f"Поле {field} не подсвечено"
        
        error = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(LoginLocators.ERROR_MESSAGE)
        )
        assert error.is_displayed(), "Сообщение об ошибке не отображается"
        assert "Ошибка" in error.text
    
    def test_registration_existing_user(self, driver):
        """Регистрация существующего пользователя"""
        # ШАГИ
        RegistrationSteps.open_login_modal(driver)
        RegistrationSteps.go_to_registration(driver)
        RegistrationSteps.fill_registration_form(
            driver, 
            EXISTING_USER["email"], 
            EXISTING_USER["password"]
        )
        RegistrationSteps.wait_for_error(driver)
        
        # ПРОВЕРКИ
        for field in ["email", "password", "submitPassword"]:
            parent = driver.find_element(*LoginLocators.error_field(field))
            error_class = parent.get_attribute("class")
            assert "input_inputError" in error_class, f"Поле {field} не подсвечено"
        
        error = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(LoginLocators.ERROR_MESSAGE)
        )
        assert error.is_displayed(), "Сообщение об ошибке не отображается"
        assert "Ошибка" in error.text