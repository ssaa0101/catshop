import pytest
from selenium.webdriver.common.by import By
import time

BASE_URL = "http://127.0.0.1:5000"


def test_full_shopping_flow(driver):
    """회원가입 -> 로그인 -> 장바구니 담기 -> 확인 (풀코스)"""

    # [중요] 브라우저 창을 최대화합니다. (메뉴가 안 숨겨지게)
    driver.maximize_window()
    driver.implicitly_wait(10)

    # ------------------------------------------------
    # 1단계: 회원가입
    # ------------------------------------------------
    print("1단계: 회원가입 진행 중...")
    driver.get(f"{BASE_URL}/register")
    time.sleep(1)

    # 매번 다른 아이디를 쓰기 위해 시간(timestamp)을 붙입니다.
    # 이렇게 하면 테스트를 여러 번 돌려도 '중복 회원' 에러가 안 납니다.
    unique_id = f"robot_{int(time.time())}"

    driver.find_element(By.NAME, "username").send_keys(unique_id)
    driver.find_element(By.NAME, "password").send_keys("1234")
    driver.find_element(By.NAME, "confirm").send_keys("1234")

    driver.find_element(By.XPATH, "//button[text()='Sign Up']").click()
    time.sleep(2)

    # ------------------------------------------------
    # 2단계: 로그인
    # ------------------------------------------------
    print("2단계: 로그인 진행 중...")

    if "Login" not in driver.title:
        driver.get(f"{BASE_URL}/login")

    driver.find_element(By.NAME, "username").send_keys(unique_id)
    driver.find_element(By.NAME, "password").send_keys("1234")

    driver.find_element(By.XPATH, "//button[text()='Login']").click()
    time.sleep(2)

    # ------------------------------------------------
    # 3단계: 장바구니 담기
    # ------------------------------------------------
    print("3단계: 쇼핑 시작!")
    if BASE_URL != driver.current_url.rstrip('/'):
        driver.get(BASE_URL)
        time.sleep(2)

    try:
        # 버튼 찾기
        btn = driver.find_element(By.CSS_SELECTOR, "form[action*='/cart/toggle/1'] button")

        # 만약 '카트에서 제거' 버튼이라면 (이전 테스트 흔적) -> 클릭해서 제거
        if "카트에서 제거" in btn.text:
            print("이미 담겨있어서 제거합니다.")
            btn.click()
            time.sleep(2)

        # '카트에 담기' 클릭
        add_btn = driver.find_element(By.CSS_SELECTOR, "form[action*='/cart/toggle/1'] button")
        add_btn.click()
        time.sleep(2)

    except Exception as e:
        pytest.fail(f"쇼핑 중 에러 발생: {e}")

    # ------------------------------------------------
    # 4단계: 결과 검증 (여기가 문제였음!)
    # ------------------------------------------------
    # 버튼이 바뀌었는지 확인
    new_btn = driver.find_element(By.CSS_SELECTOR, "form[action*='/cart/toggle/1'] button")
    assert "카트에서 제거" in new_btn.text

    print("장바구니 페이지로 이동합니다...")

    # [수정됨] 글자가 아니라 '링크 주소(href)'로 찾습니다. 훨씬 정확합니다.
    # a 태그 중에 href 주소에 '/cart'가 포함된 녀석을 찾습니다.
    driver.find_element(By.CSS_SELECTOR, "a[href*='/cart']").click()

    time.sleep(2)

    assert "장바구니" in driver.page_source
    assert "프리미엄 캣타워" in driver.page_source

    print("🎉 테스트 성공! 모든 과정 완료.")