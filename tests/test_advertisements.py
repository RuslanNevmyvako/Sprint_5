from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from locators import AdFormLocators, ModalLocators, ProfileLocators, HeaderLocators
from helpers import AdSteps


class TestAdvertisements:
    
    def test_create_ad_unauthorized(self, driver):
        """Создание объявления неавторизованным пользователем"""
        # ШАГИ
        create_ad_btn = WebDriverWait(driver, 5).until(
            expected_conditions.element_to_be_clickable(AdFormLocators.CREATE_AD_BUTTON)
        )
        create_ad_btn.click()
        
        # ПРОВЕРКИ
        assert WebDriverWait(driver, 5).until(expected_conditions.visibility_of_element_located(ModalLocators.UNAUTHORIZED_MODAL_TITLE)).is_displayed(), "Модальное окно не отображается"
    
    def test_create_ad_authorized(self, auth_driver):
        """Создание объявления авторизованным пользователем"""
        driver = auth_driver
        
        # ШАГИ
        title = AdSteps.generate_ad_title()
        AdSteps.create_ad(driver, title, "Отличное описание товара", "1500")
        
        profile_link = WebDriverWait(driver, 5).until(
            expected_conditions.presence_of_element_located(HeaderLocators.PROFILE_AVATAR)
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", profile_link)
        profile_link.click()
        
        WebDriverWait(driver, 5).until(
            expected_conditions.visibility_of_element_located(ProfileLocators.MY_ADS_TITLE)
        )
        
        AdSteps.go_to_last_page(driver)
        
        # ПРОВЕРКИ
        ad_title = WebDriverWait(driver, 10).until(
            expected_conditions.visibility_of_element_located(ProfileLocators.ad_by_title(title))
        )
        assert ad_title.is_displayed(), f"Объявление '{title}' не отображается в профиле"