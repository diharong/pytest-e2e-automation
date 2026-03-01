import pytest

class TestLogin:
    def test_정상_로그인(self, login_page):
        # 이미 로그인페이지에 와있는 ㄴ상태로 시작

        login_page.login("kim", "pass123")

        # 로그인 성공시 URL 에 "dashboard" 가 포함되어야 함
        # http://127.0.0.1:5000/dashboard
        assert "dashboard" in login_page.get_current_url()

    def test_빈_아이디_에러(self, login_page):

        login_page.login("", "pass123")

        # 에러 메세지가 화면에 나타나야함
        assert login_page.is_error_visible() is True


    def test_짧은_비밀번호_에러(self, login_page):

        login_page.login("kim", "123")

        assert login_page.is_error_visible() is True

    def test_아이디_비번_동일_에러(self, login_page):
        
        login_page.login("kim", "kim")

        assert login_page.is_error_visible() is True


    # parametrize 같은 테스트를 여러 입력값으로 반복 실행
    # 아래 4가지 케이스가 각각 독립적인 테스트로 실행됨
    @pytest.mark.parametrize("username, password", [
        ("", "pass123"),
        ("kim", "123"),
        ("kim", "kim"),
        (" ", " "),
    ])
    def test_로그인_실패_케이스들(self, login_page, username, password):

        # parametrize에서 넘어온 username, password로 로그인 시도
        login_page.login(username, password)

        #어떤 케이스든 에러 메세지가 표시되어야함
        assert login_page.is_error_visible() is True


class TestDashboard:
    # logged_in fixture를 사용.
    # → 이미 로그인된 상태에서 시작

    def test_환영메세지_표시(self, logged_in):
        welcome = logged_in.get_welcome_text()

        assert "kim" in welcome


    def test_로그아웃_후_로그인페이지(self, logged_in):

        logged_in.logout()

        assert "login" in logged_in.get_current_url()