def validate_login(username: str, password: str) -> bool:
    '''
    아주 단순한 로그인 규칙(데모용)
    - username이 비어있으면 실패
    - password 길이가 4 미만이면 실패
    - username == password 이면 실패 (너무 위험한 케이스라고 가정해봄)
    '''

    if not username:
        return False
    if len(password) < 4:
        return False
    if username == password:
        return False
    return True