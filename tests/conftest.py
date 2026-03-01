# 실패시 스크린샷 저장하는 hook 

import os
import pytest

# pytest 훅 구현
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    테스트가 실패했을 때 자동으로 스크린샷을 찍는 코드

    hookimpl = pytest 내부 이벤트에 개입하겠다는 뜻
    tryfirst=True 여러 hook 이 있을 경우 먼저 실행
    hookwrapper=True  테스트가 시작되기 전(Before)에 나타나서 대기하다가, 
                        테스트가 끝난 후(After) 결과물까지 확인하고 사라짐.

    item  : 현재 실행중인 테스트 항목
    call  : 실제 테스트 실행 단계 정보
    '''

    # yield는 pytest 기본 동작을 먼저 실행하도록 넘기는 것, 기존의 동작을 일시정지하는 것
    # hookwrapper=True 일 때 반드시 yield을 써야함
    outcome = yield # 여기서 테스트가 실제로 실행됨

    report = outcome.get_result() # 테스트 결과 가져오기


    # "테스트가 돌아가다가 에러가 나서 멈춘 그 순간에만 아래 내용을 실행해!"라는 뜻. 성공했을 때는 사진 찍을 필요가 없으니까
    if report.when == "call" and report.failed:
        '''
        report.when 은 테스트 단계를 구분하는 것
        setup / call / teardown 중에서
        지금 봐야할 것은 실제 테스트 로직이 실행된 'call' 단계
        report.failed 는 테스트 실패 여부 
        '''

        # item.funcargs 테스트 함수가 쓰고 있는 도구(fixture)들의 목록
        # .get("page", None): "그 도구 목록 중에 page(브라우저 화면)라는 도구가 있니?"라고 물어보는 것 
        # 있으면 page를 가져오고, 없으면 빈값(None)을 줘서 에러를 방지
        page = item.funcargs.get("page", None)
        if page is not None:
            
            # 사진을 저장할 폴더를 만드는 것
            # exist_ok=True: "이미 폴더가 있으면 새로 만들지 말고 그냥 넘어가(에러 내지 마)
            os.makedirs("artifacts/screenshots", exist_ok=True) 

            # 사진 파일의 이름을 정해주는 것
            screenshot_path = f"artifacts/screenshots/{item.name}.png" # 테스트 함수의 이름을 파일명으로 씀
            page.screenshot(path=screenshot_path, full_page=True) 

            print(f"\n 스크린샷 저장됨: {screenshot_path}")
