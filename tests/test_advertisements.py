from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from locators import HeaderLocators, AdFormLocators, ProfileLocators, ModalLocators


class TestAdvertisements:
    """Тесты создания объявлений"""
    
    def test_create_ad_unauthorized(self, driver):
        """Создание объявления неавторизованным пользователем"""
        create_ad_btn = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(AdFormLocators.CREATE_AD_BUTTON)
        )
        create_ad_btn.click()

        modal_title = WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(ModalLocators.UNAUTHORIZED_MODAL_TITLE)
        )
        assert modal_title.is_displayed(), "Модальное окно не отображается"
        assert "Чтобы разместить объявление, авторизуйтесь" in modal_title.text, \
            f"Неверный заголовок: '{modal_title.text}'"

    def test_create_ad_authorized(self, driver, open_login_modal, login_user, existing_user, create_ad, go_to_last_page, generate_ad_title):
        """Создание объявления авторизованным пользователем"""
        # 1. Авторизоваться
        open_login_modal()
        login_user(*existing_user)
        
        # Проверяем, что авторизация прошла
        WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located(HeaderLocators.PROFILE_AVATAR)
        )

        # 2. Создать объявление
        title = generate_ad_title
        description = "Отличное описание товара"
        price = "1500"
        
        create_ad(title, description, price)

        # 3. Перейти в профиль
        profile_link = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located(HeaderLocators.PROFILE_AVATAR)
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", profile_link)
        profile_link.click()

        # 4. Ждем загрузки профиля
        WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(ProfileLocators.MY_ADS_TITLE)
        )

        # 5. Перейти на последнюю страницу
        go_to_last_page()

        # 6. Проверить, что объявление появилось
        ad_title = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located(ProfileLocators.ad_by_title(title))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", ad_title)
        assert ad_title.is_displayed(), f"Объявление '{title}' не отображается в профиле"