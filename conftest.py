import pytest
import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from locators import LoginLocators, RegistrationFormLocators, HeaderLocators, AdFormLocators, ProfileLocators


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://qa-desk.education-services.ru")
    WebDriverWait(driver, 3)
    yield driver
    driver.quit()


@pytest.fixture
def open_login_modal(driver):
    def _open():
        login_btn = WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(LoginLocators.LOGIN_BUTTON))
        login_btn.click()
    return _open


@pytest.fixture
def go_to_registration(driver):
    def _go():
        reg_btn = WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(LoginLocators.REGISTER_BUTTON))
        reg_btn.click()
    return _go


@pytest.fixture
def generate_unique_email():
    return f"testuser_{int(time.time())}@example.com"


@pytest.fixture
def fill_registration_form(driver):
    """Фикстура для заполнения формы регистрации"""
    def _fill(email, password):
        driver.find_element(*RegistrationFormLocators.EMAIL_INPUT).send_keys(email)
        driver.find_element(*RegistrationFormLocators.PASSWORD_INPUT).send_keys(password)
        driver.find_element(*RegistrationFormLocators.CONFIRM_PASSWORD_INPUT).send_keys(password)
        driver.find_element(*LoginLocators.REGISTER_SUBMIT).click()
    return _fill


@pytest.fixture
def wait_for_error(driver):
    """Фикстура для ожидания ошибки"""
    def _wait():
        WebDriverWait(driver, 5).until(
            lambda d: "input_inputError" in d.find_element(*LoginLocators.error_field("email")).get_attribute("class")
        )
    return _wait


@pytest.fixture
def check_error_fields(driver):
    """Фикстура для проверки ошибок"""
    def _check():
        for field in ["email", "password", "submitPassword"]:
            parent = driver.find_element(*LoginLocators.error_field(field))
            assert "input_inputError" in parent.get_attribute("class"), f"{field} не подсвечен"
        
        error = WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located(LoginLocators.ERROR_MESSAGE))
        assert error.is_displayed(), "Сообщение об ошибке не отображается"
        assert "Ошибка" in error.text
    return _check


@pytest.fixture
def check_user_authorized(driver):
    """Фикстура для проверки, что пользователь авторизован"""
    def _check(expected_name="User."):
        avatar = WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located(HeaderLocators.PROFILE_AVATAR))
        assert avatar.is_displayed(), "Аватар не отображается"
        
        user_name = driver.find_element(*HeaderLocators.USER_NAME)
        assert user_name.is_displayed(), "Имя пользователя не отображается"
        assert user_name.text == expected_name, \
            f"Ожидалось '{expected_name}', получено '{user_name.text}'"
    return _check


@pytest.fixture
def login_user(driver):
    """Выполняет вход в систему"""
    def _login(email, password):
        driver.find_element(*LoginLocators.EMAIL_INPUT).send_keys(email)
        driver.find_element(*LoginLocators.PASSWORD_INPUT).send_keys(password)
        driver.find_element(*LoginLocators.LOGIN_SUBMIT).click()
    return _login


@pytest.fixture
def check_user_logged_out(driver):
    """Проверяет, что пользователь вышел"""
    def _check():
        WebDriverWait(driver, 5).until(expected_conditions.invisibility_of_element_located(HeaderLocators.PROFILE_AVATAR))
        avatars = driver.find_elements(*HeaderLocators.PROFILE_AVATAR)
        assert len(avatars) == 0, "Аватар всё еще отображается"
        
        user_names = driver.find_elements(*HeaderLocators.USER_NAME)
        assert len(user_names) == 0, "Имя пользователя всё еще отображается"
        
        login_btn = WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located(LoginLocators.LOGIN_BUTTON))
        assert login_btn.is_displayed(), "Кнопка 'Вход и регистрация' не отображается"
    return _check


@pytest.fixture
def existing_user():
    """Данные существующего пользователя"""
    return "ruslan_nev_35@gmail.com", "2517Rus"


@pytest.fixture
def logout_user(driver):
    """Выполняет выход из системы"""
    def _logout():
        logout_btn = WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(LoginLocators.LOGOUT_BUTTON))
        logout_btn.click()
    return _logout


@pytest.fixture
def create_ad(driver):
    """Создает объявление с заданными параметрами"""
    def _create(title, description, price):
        # Нажать «Разместить объявление»
        create_ad_btn = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(AdFormLocators.CREATE_AD_BUTTON)
        )
        create_ad_btn.click()

        # Заполнить поля
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

        # Выбрать категорию
        category_dropdown = driver.find_element(*AdFormLocators.CATEGORY_DROPDOWN)
        category_dropdown.click()

        category_option = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(AdFormLocators.CATEGORY_OPTION)
        )
        category_option.click()

        # Выбрать город
        city_dropdown = driver.find_element(*AdFormLocators.CITY_DROPDOWN)
        city_dropdown.click()

        city_option = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(AdFormLocators.CITY_OPTION)
        )
        city_option.click()

        # Выбрать состояние "Б/У"
        radio_used = driver.find_element(*AdFormLocators.RADIO_USED)
        radio_used.click()

        # Опубликовать
        publish_btn = driver.find_element(*AdFormLocators.PUBLISH_BUTTON)
        publish_btn.click()

        # Ждем применения
        WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(AdFormLocators.APPLY_BUTTON)
        )
    return _create


@pytest.fixture
def go_to_last_page(driver):
    """Переходит на последнюю страницу в профиле"""
    def _go():
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
    return _go


@pytest.fixture
def generate_ad_title():
    """Генерирует уникальное название для объявления"""
    return f"Мой новый товар {random.randint(100, 999)}"