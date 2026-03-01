# 로그인 성공 후 이동하는 대시보드 페이지의 요소와 동작 관리하는 페이지

from .base_page import BasePage

class DashboardPage(BasePage):

    WELCOME_TEXT = "#welcome"

    LOGOUT_BUTTON = "#logout-btn"

    def get_welcome_text(self) -> str:
        return self.page.text_content(self.WELCOME_TEXT)
    
    def logout(self):
        self.page.click(self.LOGOUT_BUTTON)