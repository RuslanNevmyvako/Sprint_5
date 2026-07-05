from selenium.webdriver.common.by import By


class LoginLocators:    
    # Кнопки
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Вход и регистрация')]")
    REGISTER_BUTTON = (By.XPATH, "//button[contains(text(), 'Нет аккаунта')]")
    REGISTER_SUBMIT = (By.XPATH, "//button[contains(text(), 'Создать аккаунт')]")

    LOGIN_SUBMIT = (By.XPATH, "//button[contains(text(), 'Войти')]")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(text(), 'Выйти')]")
    
    # Поля ввода
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    CONFIRM_PASSWORD_INPUT = (By.NAME, "submitPassword")
    
    # Сообщение об ошибке
    ERROR_MESSAGE = (By.XPATH, "//span[contains(@class, 'input_span') and contains(text(), 'Ошибка')]")
    
    # Подсветка полей
    @staticmethod
    def error_field(field_name):
        return (By.XPATH, f"//input[@name='{field_name}']/..")


class HeaderLocators:
    PROFILE_AVATAR = (By.XPATH, "//button[@class='circleSmall']")
    USER_NAME = (By.CSS_SELECTOR, "h3.profileText.name")


class RegistrationFormLocators:    
    EMAIL_INPUT = (By.NAME, "email")
    PASSWORD_INPUT = (By.NAME, "password")
    CONFIRM_PASSWORD_INPUT = (By.NAME, "submitPassword")


class AdFormLocators:
    """Локаторы для формы создания объявления"""
    CREATE_AD_BUTTON = (By.XPATH, "//button[contains(text(), 'Разместить объявление')]")
    TITLE_INPUT = (By.NAME, "name")
    DESCRIPTION_INPUT = (By.XPATH, "//textarea[@placeholder='Описание товара']")
    PRICE_INPUT = (By.NAME, "price")
    CATEGORY_DROPDOWN = (By.XPATH, "//input[@name='category']/following-sibling::button")
    CATEGORY_OPTION = (By.XPATH, "//span[contains(text(), 'Хобби')]")
    CITY_DROPDOWN = (By.XPATH, "//input[@name='city']/following-sibling::button")
    CITY_OPTION = (By.XPATH, "//span[contains(text(), 'Екатеринбург')]")
    RADIO_USED = (By.XPATH, "//div[contains(@class, 'radioUnput_shell') and contains(., 'Б/У')]//div[contains(@class, 'radioUnput_inputRegular')]")
    PUBLISH_BUTTON = (By.XPATH, "//button[contains(text(), 'Опубликовать')]")
    APPLY_BUTTON = (By.XPATH, "//button[contains(text(), 'Применить')]")


class ModalLocators:
    """Локаторы для модальных окон"""
    UNAUTHORIZED_MODAL_TITLE = (By.XPATH, "//h1[contains(text(), 'Чтобы разместить объявление, авторизуйтесь')]")


class ProfileLocators:
    """Локаторы для страницы профиля"""
    MY_ADS_TITLE = (By.XPATH, "//h1[contains(text(), 'Мои объявления')]")
    PAGINATION_TEXT = (By.XPATH, "//p[contains(@class, 'spanGlobal')]")
    NEXT_PAGE_BUTTON = (By.XPATH, "//button[contains(@class, 'arrowButton--right') and not(@disabled)]")
    
    @staticmethod
    def ad_by_title(title):
        return (By.XPATH, f"//h2[contains(text(), '{title}')]")