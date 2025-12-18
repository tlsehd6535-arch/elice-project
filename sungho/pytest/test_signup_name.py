from selenium.common.exceptions import TimeoutException
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *


# TC08: 이름 미입력
def test_space_name(driver):
    print("\n▶ TC008: 이름 공란 입력 테스트")

    email = generate_unique_username() + "@naver.com"
    password = "@qa12345"
    name = ""

    signup(driver, email, password, name)

    name_input = driver.find_element(By.XPATH, "//input[@placeholder='Name']")
    msg = driver.execute_script(
        "return arguments[0].validationMessage;", name_input
    )
    print("오류 메세지:", msg)
    assert msg !=""
    save_screenshot(driver, "signup_name", "TC08_space_name")
    print("TC008: 이름 공란 입력 테스트 성공")


# TC09: 이름 너무 김
def test_too_long_name(driver):
    print("\n▶ TC009: 긴 이름 입력 테스트")

    email = generate_unique_username() + "@naver.com"
    password = "@qa12345"
    name = "가나다라마바사아자차카타파하아야어여오유우이"

    signup(driver, email, password, name)
    save_screenshot(driver, "signup_name", "TC09_long_name_input")

    try:
        error =  WebDriverWait(driver, 2).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'your name is too long')]")
        )
    )
        assert "too long" in error.text
    except TimeoutException:
        save_screenshot(driver, "signup_name", "TC09_long_name_fail")
        print("TC009: 긴 이름 입력 테스트 실패")
        pytest.fail("이름 길이 제한 에러 메시지 없음, 정상 계정처럼 로그인이 되어버림")


# TC10: 정상 이름
def test_right_name(driver,valid_signup_data):
    print("\n▶ TC010: 정상적인 이름 입력 테스트")

    signup(driver, **valid_signup_data)

    WebDriverWait(driver, 15).until(
                EC.url_contains("/ai-helpy-chat")
            )
    icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
    assert icon.is_displayed()
    save_screenshot(driver, "signup_name", "TC10_right_name")
    print("TC010: 정상적인 이름 입력 테스트 성공")
