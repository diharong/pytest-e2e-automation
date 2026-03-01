# e2e 테스트 전용 fixture 을 모아두는 ㅏ일

'''
fixture란 ? 
"테스트 준비물을 자동으로 제공해주는 시스템"
예를 들어 로그인 페이지 테스트를 하려면 매번
1. LoginPage 객체 만들기
2. 로그인 페이지로 이동하기 를 반복해야함ㅁ
fixture에 한번만 써두면 테스트 함수가
login_page파라미터를 선언하는 것만으로 자동으로 받을 수 있음

conftest.py 는?
pytest가 자동으로 읽는 파일이다.
여기 정의된 fixture 은 같은 폴더의 모든 테스트 파일에서 사용이 가능하다.
'''

import pytest
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

# 이함수는 fixture 입니다 라고 pytest에게 알려주는 행위
@pytest.fixture
def login_page(page): #page 파라미터는 pytest-playwright 가 자동으로 제공하는 fixture
    # 브라우저 탭 1개를 의미함 , 테스트가 끝나면 자동으로 닫힘
    # 우리가 만든 login_page fixture는 이 page를 받아서
    # LoginPage 객체를 만들어 반환.
    #
    # 테스트 함수에서 def test_xxx(self, login_page): 처럼 쓰면
    # pytest가 자동으로 이 fixture를 실행해서 반환값을 넘겨줌

    lp = LoginPage(page) # loginPage 객체 생성

    lp.navigate_to()
    # 테스트 시작 전 로그인페이지로 자동이동

    return lp

@pytest.fixture
def logged_in(login_page):
    # 이 fixture 은 이미 로그인된 상태의 DashboardPage를 반환
    # 로그아웃 테스트, 대시보드 검증 테스트처럼 
    # 이미 로그인 되어있는 상태에서 시작해야하는 테스트에 사용됨

    # login_page 파라미터는 위에서 정의한 login_page fixture이다.
    # fixture가 다른 fixture를 파라미터로 받을 수 있음.
    # 이걸 "fixture 중첩" 이라고 함.
    # pytest가 알아서 login_page fixture를 먼저 실행하고 여기에 넘겨줌.

     login_page.login("kim", "pass123")

     return DashboardPage(login_page.page)

