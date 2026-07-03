from locators import LoginLocators, RegistrationFormLocators

class TestRegistration:
    """Тесты регистрации"""
    
    def test_successful_registration(self, open_login_modal, go_to_registration, generate_unique_email, fill_registration_form, check_user_authorized):
        """Регистрация нового пользователя"""
        open_login_modal()
        go_to_registration()
        
        fill_registration_form(generate_unique_email, "ValidPass123!")

        check_user_authorized()
    
    def test_registration_invalid_email(self, driver, open_login_modal, go_to_registration, wait_for_error, check_error_fields):
        """Регистрация с email не по маске"""
        open_login_modal()
        go_to_registration()
        
        driver.find_element(*RegistrationFormLocators.EMAIL_INPUT).send_keys("invalid-email")
        driver.find_element(*LoginLocators.REGISTER_SUBMIT).click()
        
        wait_for_error()
        check_error_fields()
    
    def test_registration_existing_user(self, open_login_modal, go_to_registration,fill_registration_form, wait_for_error, check_error_fields):
        """Регистрация уже существующего пользователя"""
        open_login_modal()
        go_to_registration()
        
        fill_registration_form("ruslan_nev_35@gmail.com", "2517Rus")
        
        wait_for_error()
        check_error_fields()