import pytest  # <-- 이 줄이 없어서 에러가 났던 겁니다!
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 기존 Flask 테스트용 임포트
from app import app, USERS


# ---------------------------------------------------------
# 1. Flask 내부 로직 테스트용 (로그인, 회원가입 등)
# ---------------------------------------------------------
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'

    # 데이터 보존을 위해 백업
    original_users = USERS.copy()

    with app.test_client() as client:
        yield client

    # 테스트 후 복구
    USERS.clear()
    USERS.update(original_users)


@pytest.fixture
def login_test_env(client):
    test_username = "test_butler"
    test_password = "password123"
    USERS[test_username] = {"password": test_password}
    return client, test_username, test_password


# ---------------------------------------------------------
# 2. Selenium 브라우저 테스트용 (장바구니, 결제 클릭 등)
# ---------------------------------------------------------
@pytest.fixture(scope="module")
def driver():
    """Selenium 테스트를 위한 크롬 브라우저 실행기"""
    # 크롬 드라이버 자동 설치 및 설정
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    # (옵션) 브라우저가 꺼지지 않고 유지되게 하려면 아래 옵션 추가 가능
    # options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(3)  # 요소를 찾을 때 최대 3초 대기

    yield driver

    driver.quit()  # 테스트 끝나면 브라우저 닫기