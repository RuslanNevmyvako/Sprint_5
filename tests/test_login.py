class TestLogin:
    def test_login_success(self, open_login_modal, login_user, check_user_authorized, existing_user):
        open_login_modal()
        login_user(*existing_user)
        check_user_authorized()
    
    def test_logout(self, open_login_modal, login_user, check_user_authorized, check_user_logged_out, existing_user, logout_user):
        open_login_modal()
        login_user(*existing_user)
        check_user_authorized()

        logout_user()
        check_user_logged_out()