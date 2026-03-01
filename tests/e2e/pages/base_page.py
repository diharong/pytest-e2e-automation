# 모든 페이지 클래스의 부모 클래스
# 왜 만들까?
# login_page, dashboard_page 둘 다 공통적으로 쓰는 기능 (이동, 스크린샷 기능 등)
# 여기 한 곳에 모아두면 각 페이지 클래스에서 중복 코드가 없어짐 

class BasePage:
    def __init__(self, page):
        '''
         __init__ = 클래스로 객체를 만들 때 자동으로 실행되는 함수.
        
        page 파라미터는 Playwright의 "브라우저 탭 1개"를 나타냄.
        pytest-playwright의 page fixture가 이걸 자동으로 넘겨줌.
        
        self.page = page 로 저장하면
        이 클래스의 모든 메서드에서 self.page 로 접근할 수 있음.
        '''
        self.page = page

    def navigate(self, url: str):
        # 받은 url 주소로 브라우저가 이동
        self.page.goto(url)

    def get_current_url(self) -> str:
        return self.page.url
    
    def take_screenshot(self, name:str):
        self.page.screenshot(path=f"artifacts/screenshots/{name}.png")



    
