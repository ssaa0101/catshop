import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

BASE_URL = "http://127.0.0.1:5000"


def test_full_checkout_flow(driver):
    """회원가입 -> 장바구니 -> 결제 정보 입력 -> 완료 메시지 확인"""

    # 1. 브라우저 설정
    driver.maximize_window()  # 전체 화면
    driver.implicitly_wait(10)  # 10초 대기 설정

    # ------------------------------------------------
    # 1단계: 회원가입 & 로그인 (결제하려면 회원이여야 함)
    # ------------------------------------------------
    print("1단계: 회원가입 및 로그인 진행...")
    driver.get(f"{BASE_URL}/register")

    # 매번 새로운 아이디 생성 (충돌 방지)
    unique_id = f"buyer_{int(time.time())}"

    driver.find_element(By.NAME, "username").send_keys(unique_id)
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.NAME, "confirm").send_keys("1234")
    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    time.sleep(1)

    # 로그인 페이지로 이동되었을 것임
    if "Login" not in driver.title:
        driver.get(f"{BASE_URL}/login")

    driver.find_element(By.NAME, "username").send_keys(unique_id)
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(1)

    # ------------------------------------------------
    # 2단계: 상품 담기 (장바구니가 비면 결제를 못함)
    # ------------------------------------------------
    print("2단계: 상품 담기...")
    # 메인 페이지로 이동 확인
    if BASE_URL != driver.current_url.rstrip('/'):
        driver.get(BASE_URL)

    try:
        # '카트에 담기' 버튼 찾아서 클릭
        add_btn = driver.find_element(By.CSS_SELECTOR, "form[action*='/cart/toggle/1'] button")

        # 혹시 '제거' 버튼이면(이미 담김) 그냥 둠, 아니면 클릭
        if "카트에 담기" in add_btn.text:
            add_btn.click()
            time.sleep(1)
    except Exception as e:
        pytest.fail(f"상품 담기 실패: {e}")

    # ------------------------------------------------
    # 3단계: 장바구니 -> 결제 페이지 이동
    # ------------------------------------------------
    print("3단계: 결제 페이지로 이동...")
    # 상단 메뉴의 Cart 링크 클릭 (Partial Link Text 사용)
    driver.find_element(By.PARTIAL_LINK_TEXT, "Cart").click()
    time.sleep(1)

    # '결제하기' 버튼 클릭 (초록색 버튼)
    # CSS Selector 설명: a 태그이면서 클래스에 'btn-success'가 있는 요소
    driver.find_element(By.CSS_SELECTOR, "a.btn-success").click()
    time.sleep(1)

    # ------------------------------------------------
    # 4단계: 결제 정보 입력 (폼 채우기)
    # ------------------------------------------------
    print("4단계: 배송 정보 입력 중...")

    # checkout.html에 있는 name 속성을 찾아서 입력
    driver.find_element(By.NAME, "name").send_keys("테스트 구매자")
    driver.find_element(By.NAME, "phone").send_keys("010-1234-5678")
    driver.find_element(By.NAME, "address").send_keys("서울시 강남구 테헤란로 123")

    # ------------------------------------------------
    # 5단계: 결제 완료 및 검증
    # ------------------------------------------------
    print("5단계: 결제 버튼 클릭!")

    # '결제 완료' 버튼 클릭
    driver.find_element(By.XPATH, "//button[text()='결제 완료']").click()
    time.sleep(2)  # 서버 처리 대기

    # 결과 확인: 메인 페이지로 돌아왔고, 성공 메시지가 떠야 함
    page_source = driver.page_source

    # app.py의 flash 메시지: "결제가 완료되었습니다! 주문이 접수되었습니다."
    if "결제가 완료되었습니다" in page_source:
        print("🎉 결제 테스트 성공!")
    else:
        print(page_source)  # 디버깅용 출력
        pytest.fail("결제 완료 메시지를 찾을 수 없습니다.")