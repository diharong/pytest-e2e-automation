import pytest
from app.auth import validate_login

def test_validate_login_success():
    # 정상 케이스 : username 존재 + password 길이 충분 + 서로 다름
    assert validate_login("kim", "pass123") is True

def test_validate_login_fail_empty_username():
    # username 공백
    assert validate_login("", "pass123") is False

def test_validate_login_fail_short_password():
    assert validate_login("kim", "123") is False

def test_validate_login_fail_same_username_password():
    assert validate_login("kim", "kim") is False


# 같은 검증을 데이터만 바꿔서 반복하고 싶을 때 : parametrize사용
@pytest.mark.parametrize(
    "username,password,expected",
    [
        ("kim", "pass123", True),
        ("", "pass123", False),
        ("kim", "123", False),
        ("kim", "kim", False),
    ]
)
def test_validate_login_parametrized(username, password, expected):
    assert validate_login(username,password) is expected