import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from locators import LoginLocators, RegistrationFormLocators, AdFormLocators, ProfileLocators


class RegistrationSteps:
    """Шаги для тестов регистрации"""
    
    @staticmethod
    def open_login_modal(driver):
        login_btn = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(LoginLocators.LOGIN_BUTTON)
        )
        login_btn.click()
    
    @staticmethod
    def go_to_registration(driver):
        reg_btn = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(LoginLocators.REGISTER_BUTTON)
        )
        reg_btn.click()
    
    @staticmethod
    def fill_registration_form(driver, email, password):
        driver.find_element(*RegistrationFormLocators.EMAIL_INPUT).send_keys(email)
        driver.find_element(*RegistrationFormLocators.PASSWORD_INPUT).send_keys(password)
        driver.find_element(*RegistrationFormLocators.CONFIRM_PASSWORD_INPUT).send_keys(password)
        driver.find_element(*LoginLocators.REGISTER_SUBMIT).click()
    
    @staticmethod
    def generate_unique_email():
        return f"testuser_{int(time.time())}@example.com"
    
    @staticmethod
    def wait_for_error(driver):
        WebDriverWait(driver, 5).until(
            lambda d: "input_inputError" in d.find_element(*LoginLocators.error_field("email")).get_attribute("class")
        )


class LoginSteps:
    """Шаги для тестов авторизации"""

    @staticmethod
    def open_login_modal(driver):
        """Открывает модальное окно входа"""
        login_btn = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(LoginLocators.LOGIN_BUTTON)
        )
        login_btn.click()

        WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(LoginLocators.EMAIL_INPUT)
        )
    
    @staticmethod
    def login(driver, email, password):
        driver.find_element(*LoginLocators.EMAIL_INPUT).send_keys(email)
        driver.find_element(*LoginLocators.PASSWORD_INPUT).send_keys(password)
        driver.find_element(*LoginLocators.LOGIN_SUBMIT).click()
    
    @staticmethod
    def logout(driver):
        logout_btn = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(LoginLocators.LOGOUT_BUTTON)
        )
        logout_btn.click()


class AdSteps:
    """Шаги для тестов объявлений"""
    
    @staticmethod
    def create_ad(driver, title, description, price):
        create_ad_btn = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(AdFormLocators.CREATE_AD_BUTTON)
        )
        create_ad_btn.click()

        title_input = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(AdFormLocators.TITLE_INPUT)
        )
        title_input.send_keys(title)

        description_input = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(AdFormLocators.DESCRIPTION_INPUT)
        )
        description_input.send_keys(description)

        price_input = driver.find_element(*AdFormLocators.PRICE_INPUT)
        price_input.send_keys(price)

        category_dropdown = driver.find_element(*AdFormLocators.CATEGORY_DROPDOWN)
        category_dropdown.click()

        category_option = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(AdFormLocators.CATEGORY_OPTION)
        )
        category_option.click()

        city_dropdown = driver.find_element(*AdFormLocators.CITY_DROPDOWN)
        city_dropdown.click()

        city_option = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(AdFormLocators.CITY_OPTION)
        )
        city_option.click()

        radio_used = driver.find_element(*AdFormLocators.RADIO_USED)
        radio_used.click()

        publish_btn = driver.find_element(*AdFormLocators.PUBLISH_BUTTON)
        publish_btn.click()

        WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(AdFormLocators.APPLY_BUTTON)
        )
    
    @staticmethod
    def go_to_last_page(driver):
        page_info = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located(ProfileLocators.PAGINATION_TEXT)
        ).text
        last_page = int(page_info.split()[2])
        
        for _ in range(last_page - 1):
            next_btn = WebDriverWait(driver, 5).until(
                expected_conditions.element_to_be_clickable(ProfileLocators.NEXT_PAGE_BUTTON)
            )
            next_btn.click()
            time.sleep(0.5)
    
    @staticmethod
    def generate_ad_title():
        return f"Мой новый товар {random.randint(100, 999)}"