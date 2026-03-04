# pytest + Playwright 테스트 자동화 파이프라인

![CI](https://github.com/diharong/pytest-e2e-automation/actions/workflows/test.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![pytest](https://img.shields.io/badge/pytest-8.x-green)
![Playwright](https://img.shields.io/badge/Playwright-latest-orange)

> Flask 웹앱을 직접 만들고, pytest + Playwright로 GUI 테스트를 자동화하고,
> GitHub Actions로 CI 파이프라인까지 연결한 프로젝트입니다.

📖 **[블로그 시리즈 전체 보기](https://diharong.github.io/pytest-e2e-automation/)**

---

## 📌 프로젝트 개요

단순히 테스트 라이브러리 사용법을 익히는 것을 넘어,
**테스트 대상 서비스(Flask 앱)부터 자동화 프레임워크(pytest + Playwright), CI 파이프라인까지 직접 설계하고 연결**했습니다.

- 테스트하기 좋은 구조로 서비스를 설계하고
- 단위 테스트로 로직을 검증하고
- GUI 자동화로 사용자 시나리오를 검증하고
- CI로 push마다 자동 실행되도록 파이프라인을 구성하는

전체 흐름을 한 프로젝트에 담았습니다.

---

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
| 테스트 패턴 | Page Object Model (POM) |
| CI 파이프라인 | GitHub Actions |

---

## 📁 프로젝트 구조

```
pytest-e2e-automation/
├── .github/
│   └── workflows/
│       └── test.yml         # CI: push 시 자동 테스트 실행
├── app/
│   ├── auth.py              # 로그인 검증 로직 (UI와 분리)
│   ├── server.py            # Flask 웹 서버
│   └── templates/
│       ├── login.html
│       └── dashboard.html
├── tests/
│   ├── conftest.py          # 실패 시 스크린샷 자동 저장 (pytest hook)
│   ├── unit/
│   │   └── test_auth.py     # 단위 테스트
│   └── e2e/
│       ├── conftest.py      # 브라우저 fixture
│       ├── pages/           # Page Object Model
│       │   ├── base_page.py
│       │   ├── login_page.py
│       │   └── dashboard_page.py
│       └── test_login_e2e.py
├── docs/                    # GitHub Pages 블로그
├── pytest.ini
└── requirements.txt
```

---

## ✅ 테스트 항목

### 단위 테스트 (Unit Test) — 8개
브라우저 없이 로그인 검증 로직만 빠르게 검증합니다.

| 테스트 | 설명 |
|---|---|
| test_validate_login_success | 정상 로그인 성공 |
| test_validate_login_fail_empty_username | 빈 아이디 거부 |
| test_validate_login_fail_short_password | 4자 미만 비밀번호 거부 |
| test_validate_login_fail_same_username_password | 아이디=비밀번호 거부 |
| test_validate_login_parametrized | 경계값 4가지 케이스 한번에 검증 |

### E2E GUI 자동화 테스트 — 10개
실제 브라우저를 켜서 사용자처럼 클릭/입력하여 검증합니다.

| 테스트 | 설명 |
|---|---|
| test_정상_로그인 | 올바른 계정으로 로그인 후 dashboard 이동 확인 |
| test_빈_아이디_에러 | 빈 아이디로 시도 시 에러 메시지 표시 확인 |
| test_짧은_비밀번호_에러 | 4자 미만 비밀번호로 시도 시 에러 메시지 확인 |
| test_아이디_비번_동일_에러 | 아이디=비밀번호로 시도 시 에러 메시지 확인 |
| test_로그인_실패_케이스들 | parametrize로 4가지 실패 케이스 한번에 검증 |
| test_환영메세지_표시 | 로그인 후 환영 메시지에 아이디 포함 확인 |
| test_로그아웃_후_로그인페이지 | 로그아웃 후 로그인 페이지로 이동 확인 |

---

## 🔑 핵심 구현 포인트

### 1. Page Object Model (POM)
셀렉터를 테스트 파일에 직접 쓰지 않고 `pages/` 폴더에서 관리합니다.
HTML이 바뀌어도 page 파일 하나만 수정하면 됩니다.

```python
# ❌ POM 없이 — 셀렉터가 테스트 코드에 직접 박혀있음
page.fill("#username", "kim")
page.fill("#password", "pass123")
page.click("#login-btn")

# ✅ POM 적용 후 — 테스트는 시나리오에만 집중
login_page.login("kim", "pass123")
```

### 2. pytest fixture
브라우저 준비/정리를 자동화해서 테스트 함수는 검증 로직에만 집중합니다.

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
pytest hook을 활용해서 테스트 실패 시 화면을 자동 캡처합니다.
CI 환경(headless)에서도 실패 원인을 GitHub artifacts에서 바로 확인할 수 있습니다.

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

### 4. GitHub Actions CI 파이프라인
`main` 브랜치에 push하면 자동으로 18개 테스트가 실행됩니다.

```yaml
on:
  push:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements.txt
      - run: python -m playwright install --with-deps chromium
      - run: cd app && python server.py &  # 백그라운드 실행
      - run: pytest tests/ -v
      - if: failure()
        uses: actions/upload-artifact@v3   # 실패 시 스크린샷 업로드
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
| 3편 | [GitHub Actions로 CI 파이프라인 구축하기](https://diharong.github.io/pytest-e2e-automation/part3.html) | push → 자동 테스트 → artifacts 수집 |
