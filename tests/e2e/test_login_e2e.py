import pytest

BASE_URL = "http://127.0.0.1:5000"

# pytest 마커
# 왜 쓰냐? e2e 테스트만 따로 실행하기 위해서
@pytest.mark.e2e
def test_login_success(page):
    '''
    로그인 성공 시나리오:
    1) /login 접속
    2) username/password 입력
    3) 로그인 버튼 클릭
    4) dashboard로 이동했고, 환영 문구가 보이는지 검증
    '''

    # 브라우저가 해당 URL로 이동
    # page는 pytest-playwright가 제공하는 fixture (브라우저 탭 1개라고 생각하면 됨)
    page.goto(f"{BASE_URL}/login")

    page.fill("#username", "kim") # input id = "username"
    page.fill("#password", "pass123") # input id = "password"

    # id="login-btn" 버튼 클릭
    page.click("#login-btn")


    # 로그인 성공 시 dashboard 페이지로 이동하고
    # id="welcome" 요소가 존재함
    # locator는 요소를 "찾기 위한 객체"를 만드는 것
    #dashboard로 이동하면 h1#welcome 이 보임
    welcome = page.locator("#welcome")
    except_text = "Welcome, kim"
    assert welcome.inner_text() == except_text

@pytest.mark.e2e
def test_login_fail_shows_error(page):
    '''
    로그인 실패 시나리오
    1) /login 접속
    2) 잘못된 값 입력 (ex. username 공백)
    3) 로그인 버튼 클릭
    4) 에러 메세지가 화면에 나타나는지 검증
    '''

    # 로그인 페이지 접속
    page.goto(f"{BASE_URL}/login")
    # username 비워서 실패 유도
    page.fill("#username", "")

    # 비밀번호는 정상값
    page.fill("#password", "pass123")

    # 로그인 버튼 클릭
    page.click("#login-btn")

    # id = "error" 요소를 찾기 위한 locator 생성
    error = page.locator("#error")

    # 에러메세지가 화면에 실제로 보이는지 확인
    # is_visible()은 요소가 DOM에 있고, 화면에 표시되는지 확인
    assert error.is_visible() is True


@pytest.mark.e2e
def test_스크린샷_저장_확인용(page):
    """
    이 테스트는 일부러 실패시켜서
    artifacts/screenshots/ 폴더에 스크린샷이 찍히는지 확인하는 용도예요.
    확인 후 삭제해도 됩니다.
    """
    page.goto(f"{BASE_URL}/login")

    # 로그인 성공하면 화면에 "Welcome, kim" 이 나옴
    # 근데 아래에서 "kim" 이 아닌 엉뚱한 이름을 기대하면 → 실패
    page.fill("#username", "kim")
    page.fill("#password", "pass123")
    page.click("#login-btn")

    welcome = page.locator("#welcome")
    actual = welcome.inner_text()       # 실제값: "Welcome, kim"
    expected = "Welcome, 홍길동"         # 기대값: "Welcome, 홍길동" (없는 이름)

    # actual != expected 이므로 실패
    assert actual == expected




