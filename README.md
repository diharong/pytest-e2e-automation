# pytest + Playwright 테스트 자동화 파이프라인

![CI](https://github.com/diharong/pytest-e2e-automation/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![pytest](https://img.shields.io/badge/pytest-8.x-green)
![Playwright](https://img.shields.io/badge/Playwright-latest-orange)

> Flask 웹앱을 만들고, pytest + Playwright로 GUI 테스트를 자동화한 뒤
> GitHub Actions로 테스트가 자동 실행되도록 연결한 프로젝트입니다.

📖 **[블로그 시리즈 전체 보기](https://diharong.github.io/pytest-e2e-automation/)**

---

## 📌 프로젝트 개요

이 프로젝트는 테스트 코드를 작성하는 것에서 끝나는 것이 아니라,  
**테스트 대상 서비스와 테스트 실행 환경을 함께 구성해보는 것**을 목표로 만들었습니다.

간단한 Flask 웹 애플리케이션을 만들고,

- pytest로 **로직을 단위 테스트로 검증하고**
- Playwright로 **브라우저 기반 GUI 테스트를 작성하고**
- GitHub Actions로 **코드 변경 시 테스트가 자동 실행되도록** 구성했습니다.

---

## 🎬 Demo

Playwright가 브라우저를 열고 로그인 흐름을 자동으로 테스트하는 모습입니다.




## 🔄 전체 파이프라인

```
Flask 앱 설계 → 단위 테스트(8개) → E2E 자동화(10개) → POM 패턴 적용 → CI 파이프라인
     ↓                                                                         ↓
테스트하기 좋은 구조                                              push → 18개 자동 실행
```

---

## 🛠 기술 스택

| 역할 | 기술 |
|---|---|
| 웹 서버 | Flask |
| 단위 테스트 | pytest |
| GUI 자동화 | Playwright + pytest-playwright |
| 테스트 구조 | Page Object Model (POM) |
| CI | GitHub Actions |

---

## 📁 프로젝트 구조

```
pytest-e2e-automation/
├── .github/
│   └── workflows/
│       └── test.yml         
├── app/
│   ├── auth.py              
│   ├── server.py            
│   └── templates/
│       ├── login.html
│       └── dashboard.html
├── tests/
│   ├── conftest.py          
│   ├── unit/
│   │   └── test_auth.py     
│   └── e2e/
│       ├── conftest.py      
│       ├── pages/           
│       │   ├── base_page.py
│       │   ├── login_page.py
│       │   └── dashboard_page.py
│       └── test_login_e2e.py
├── docs/                   
├── pytest.ini
└── requirements.txt
```

---

## ✅ 테스트 항목

### 단위 테스트 (Unit Test) — 8개
브라우저 없이 로그인 검증 로직만 검증합니다.

| 테스트 | 설명 |
|---|---|
| test_validate_login_success | 정상 로그인 성공 |
| test_validate_login_fail_empty_username | 빈 아이디 거부 |
| test_validate_login_fail_short_password | 4자 미만 비밀번호 거부 |
| test_validate_login_fail_same_username_password | 아이디=비밀번호 거부 |
| test_validate_login_parametrized | 여러 입력값을 한번에 검증 |

### E2E GUI 테스트 — 10개
브라우저를 실행해서 실제 사용자 동작처럼 로그인 과정을 확인합니다.

| 테스트 | 설명 |
|---|---|
| test_정상_로그인 | 로그인 후 dashboard 이동 확인 |
| test_빈_아이디_에러 | 빈 아이디 입력 시 에러 메시지 확인 |
| test_짧은_비밀번호_에러 | 4자 미만 비밀번호로 입력 시 에러 메시지 확인 |
| test_아이디_비번_동일_에러 | 아이디=비밀번호 입력 시 에러 메시지 확인 |
| test_로그인_실패_케이스들 | 여러 실패 케이스를 parametrize로 확인 |
| test_환영메세지_표시 | 로그인 후 환영 메시지 확인 |
| test_로그아웃_후_로그인페이지 | 로그아웃 후 로그인 페이지로 이동 확인 |

---

## 🔑 구현 포인트

### 1. Page Object Model (POM)
화면 요소 셀렉터를 테스트 코드에 직접 쓰지 않고  
`pages/` 폴더에서 관리하도록 구성했습니다.

HTML이 변경되면 해당 페이지 파일만 수정하면 됩니다.

```python
# ❌ POM 없이 — 셀렉터가 테스트 코드에 직접 사용
page.fill("#username", "kim")
page.fill("#password", "pass123")
page.click("#login-btn")

# ✅ POM 적용 
login_page.login("kim", "pass123")
```

### 2. pytest fixture
브라우저 생성과 종료를 fixture에서 처리해서 테스트 함수에서는 검증 로직만 작성하도록 했습니다.

```python
@pytest.fixture
def login_page(page):
    lp = LoginPage(page)
    lp.navigate_to()
    return lp

def test_정상_로그인(self, login_page):
    login_page.login("kim", "pass123")
    assert "dashboard" in login_page.get_current_url()
```

### 3. 실패 시 스크린샷 자동 저장
pytest hook을 사용해서 테스트가 실패하면
현재 화면을 자동으로 캡처하도록 했습니다.

```python
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page", None)
        if page is not None:
            page.screenshot(path=f"artifacts/screenshots/{item.name}.png")
```

### 4. GitHub Actions 연결하기
코드를 push하면 테스트가 자동으로 실행되도록 설정했습니다.

```yaml
on:
  push:
    branches: [ master ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: python -m playwright install --with-deps chromium
      - run: cd app && python server.py &  
      - run: pytest tests/ -v
      - if: failure()
        uses: actions/upload-artifact@v3   
```

---

## 🚀 실행 방법

```bash
# 1. 클론 및 환경 설치
git clone https://github.com/diharong/pytest-e2e-automation.git
cd pytest-e2e-automation

python -m venv .venv
source .venv/bin/activate       # Mac/Linux
# .\.venv\Scripts\activate      # Windows

pip install -r requirements.txt
python -m playwright install

# 2. Flask 서버 실행 (별도 터미널)
cd app && python server.py

# 3. 테스트 실행
pytest tests/ -v                # 전체 실행
pytest tests/unit/ -v           # 단위 테스트만
pytest tests/e2e/ -v --headed   # GUI 자동화 (브라우저 표시)
pytest -m smoke                 # smoke 테스트만
```

---

## 📊 테스트 결과

```
collected 18 items

tests/e2e/test_login_e2e.py::TestLogin::test_정상_로그인[chromium]                PASSED
tests/e2e/test_login_e2e.py::TestLogin::test_빈_아이디_에러[chromium]              PASSED
tests/e2e/test_login_e2e.py::TestLogin::test_짧은_비밀번호_에러[chromium]          PASSED
tests/e2e/test_login_e2e.py::TestLogin::test_아이디_비번_동일_에러[chromium]       PASSED
tests/e2e/test_login_e2e.py::TestLogin::test_로그인_실패_케이스들[chromium-...]    PASSED
tests/e2e/test_login_e2e.py::TestDashboard::test_환영메세지_표시[chromium]         PASSED
tests/e2e/test_login_e2e.py::TestDashboard::test_로그아웃_후_로그인페이지[chromium] PASSED
tests/unit/test_auth.py::test_validate_login_success                              PASSED
...

18 passed in 5.15s
```

---

## 📝 기술 블로그 시리즈

구현 과정을 3편으로 상세히 정리했습니다.

| 편 | 제목 | 주요 내용 |
|---|---|---|
| 1편 | [pytest + Playwright로 GUI 테스트 자동화하기](https://diharong.github.io/pytest-e2e-automation/part1.html) | Flask 앱 설계, 단위 테스트, E2E 자동화, 스크린샷 저장 |
| 2편 | [Page Object Model(POM) 패턴 적용하기](https://diharong.github.io/pytest-e2e-automation/part2.html) | 셀렉터 분리, BasePage 상속, fixture 중첩 |
| 3편 | [GitHub Actions로 CI 연결하기](https://diharong.github.io/pytest-e2e-automation/part3.html) | push → 자동 테스트 → artifacts 수집 |