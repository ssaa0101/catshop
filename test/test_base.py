import pytest
from selenium.webdriver.common.by import By
import time

BASE_URL = "http://127.0.0.1:5000"


def test_base_layout_visuals(driver):
    """[Selenium] 기본 레이아웃(네비게이션, 타이틀) 시각적 검증"""
    driver.maximize_window()
    driver.get(BASE_URL)
    driver.implicitly_wait(5)

    print("사이트 접속 및 타이틀 확인...")
    # 1. 브라우저 탭 제목 확인
    assert "Resona Cat Shop" in driver.title

    # 2. 상단 로고(브랜드명) 확인
    brand = driver.find_element(By.CLASS_NAME, "navbar-brand")
    assert "RESONA CAT SHOP" in brand.text

    # 3. 비로그인 상태일 때 메뉴 확인 (Login, Sign Up)
    navbar_text = driver.find_element(By.ID, "mainNav").text
    assert "Login" in navbar_text
    assert "Sign Up" in navbar_text

    # 4. 푸터나 메인 컨테이너가 잘 잡혀있는지 확인
    main_area = driver.find_element(By.TAG_NAME, "main")
    assert main_area.is_displayed()

    print("✅ Base 레이아웃 검증 완료")