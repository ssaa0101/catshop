import pytest
from selenium.webdriver.common.by import By
import time

BASE_URL = "http://127.0.0.1:5000"


def test_product_detail_navigation(driver):
    """[Selenium] 상품 상세 페이지 이동 및 복귀 테스트"""
    driver.maximize_window()
    driver.get(BASE_URL)
    driver.implicitly_wait(5)

    # 1. 두 번째 상품(터널 놀이 텐트)의 상세보기 버튼 클릭
    # (btn-outline-secondary 클래스를 가진 버튼들 중 1번째 인덱스)
    print("두 번째 상품 상세보기 클릭...")
    buttons = driver.find_elements(By.CSS_SELECTOR, "a.btn-outline-secondary")
    buttons[1].click()

    time.sleep(2)

    # 2. 상세 페이지 내용 검증
    # 제목(h1) 확인
    title = driver.find_element(By.TAG_NAME, "h1").text
    assert "터널 놀이 텐트" in title

    # 가격 및 설명 확인
    assert "39,000원" in driver.page_source
    assert "PlayLand" in driver.page_source

    # 3. '메인으로' 링크 클릭
    print("메인으로 복귀 시도...")
    driver.find_element(By.PARTIAL_LINK_TEXT, "메인으로").click()
    time.sleep(1)

    # 4. URL 확인 (메인으로 잘 왔는지)
    assert BASE_URL == driver.current_url.rstrip('/')

    print("✅ 상품 상세 네비게이션 검증 완료")