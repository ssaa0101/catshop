import pytest
from selenium.webdriver.common.by import By
import time

BASE_URL = "http://127.0.0.1:5000"


def test_login_failure_scenario(driver):
    """[Selenium] 로그인 실패 시 에러 메시지 출력 확인"""
    driver.maximize_window()
    driver.get(f"{BASE_URL}/login")
    driver.implicitly_wait(5)

    # 1. 로그인 폼 요소 확인
    driver.find_element(By.NAME, "username")
    driver.find_element(By.NAME, "password")

    # 2. 일부러 틀린 정보 입력
    print("로그인 실패 테스트 시도...")
    driver.find_element(By.NAME, "username").send_keys("ghost_user")
    driver.find_element(By.NAME, "password").send_keys("wrong_pw")

    # 3. 로그인 버튼 클릭
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(1)

    # 4. 'alert-danger' (빨간색 에러 박스) 확인
    error_alert = driver.find_element(By.CLASS_NAME, "alert-danger")
    print(f"감지된 에러 메시지: {error_alert.text}")
    assert "아이디 또는 비밀번호가 올바르지 않습니다" in error_alert.text

    print("✅ 로그인 예외 처리 검증 완료")