import pytest
from selenium.webdriver.common.by import By
import time

BASE_URL = "http://127.0.0.1:5000"


def test_register_password_mismatch(driver):
    """[Selenium] 회원가입 비밀번호 불일치 방어 확인"""
    driver.maximize_window()
    driver.get(f"{BASE_URL}/register")
    driver.implicitly_wait(5)

    assert "Sign Up" in driver.title

    # 1. 폼 입력 (비밀번호와 확인을 다르게 입력)
    print("비밀번호 불일치 입력 시도...")
    driver.find_element(By.NAME, "username").send_keys("fail_man")
    driver.find_element(By.NAME, "password").send_keys("pass123")
    driver.find_element(By.NAME, "confirm").send_keys("pass999")  # 다르게!

    # 2. 가입 버튼 클릭
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    time.sleep(1)

    # 3. 에러 메시지 확인
    error_alert = driver.find_element(By.CLASS_NAME, "alert-danger")
    print(f"감지된 에러 메시지: {error_alert.text}")
    assert "비밀번호가 일치하지 않습니다" in error_alert.text

    print("✅ 회원가입 방어 로직 검증 완료")