# 로그인 페이지에서 할 수 있는 모든 동작과
# 페이지에 있는 요소들의 "주소(셀렉터)" 를 여기서 관리

'''
셀렉터란?
Playwright 가 HTML 에서 요소를 찾을 때 쓰는 주소
예 : "#username" -> id 가 "username" 인 input 태그를 찾아라 
'''

'''
왜 셀렉터를 이 파일에서만 관리할까?
나중에 html 이 바뀌어서 id="username" -> id="user-input" 이 되면
이 파일의 USERNAME_INPUT 값만 바꾸면 된다.
테스트 파일은 손댈 필요 xx
반대로 셀렉터가 테스트 파일에 흩어져 있으면 모든 파일을 일일이 찾아서 바꿔야함
'''

from .base_page import BasePage

class LoginPage(BasePage):
    '''
    상수로 쓰는 이유
    "#username" 같은 문자열을 코드 여러 곳에 직접 쓰면
    한꺼번에 바꾸기 힘듦
    상수로 하나만 바꾸며 그걸 쓰는 모든 곳이 자동으로 바뀔 수 있음
    '''

    URL = "http://127.0.0.1:5000/login"

    USERNAME_INPUT = "#username"

    PASSWORD_INPUT = "#password"

    LOGIN_BUTTON = "#login-btn"

    ERROR_MESSAGE = "#error"

    def navigate_to(self):
        #로그인페이지 url로 이동
        self.navigate(self.URL)

    def login(self, username: str, password: str):
        # 로그인하는 동작전체(입력->클릭) 을 하나의 메서드로 묶어 중복 없애기
        # fill(셀렉터, 값) 해당 input 태그에 텍스트를 입력함
        self.page.fill(self.USERNAME_INPUT, username)
        self.page.fill(self.PASSWORD_INPUT, password)

        # 버튼 클릭
        self.page.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        return self.page.text_content(self.ERROR_MESSAGE)
    
    # 에러메세지가 화면에 보이는지 확인
    def is_error_visible(self) -> bool:
        return self.page.is_visible(self.ERROR_MESSAGE)
    
