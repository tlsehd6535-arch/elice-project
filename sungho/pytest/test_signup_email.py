from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *

# TC1 이메일 공란 회원가입 테스트
def test_space_email(driver):
    email = ""
    password = "@qa12345"
    name = "김성호"

    signup(driver, email, password, name)

    email_input = driver.find_element(By.XPATH, "//input[@placeholder='Email']")
    msg = driver.execute_script(
        "return arguments[0].validationMessage;", email_input
    )
    time.sleep(1)

    assert msg != ""  # 브라우저 validation 발생 확인


# TC2 잘못된 이메일 형식
def test_wrong_email_type(driver):
    email = generate_unique_username() + "naver.com"
    password = "@qa12345"
    name = "김성호"

    signup(driver, email, password, name)

    error = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Email address is incorrect.')]")
        )
    )

    assert "Email address is incorrect." in error.text
    save_screenshot(driver, "signup_email", "TC02_wrong_email_type")


# TC3 정상 회원가입
def test_right_signup(driver,valid_signup_data):
    

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
    save_screenshot(driver, "signup_email", "TC03_signup_success")

# TC4 중복 이메일 회원가입
def test_duplicate_email(driver,valid_signup_data):

    signup(driver,**valid_signup_data)

    open_signup_page(driver)
    fill_signup_form(driver,valid_signup_data["email"])

    error = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located(
            (By.XPATH, "//p[contains(text(), 'This is an already registered email address.')]")
        )
    )

    assert "already registered email" in error.text
    save_screenshot(driver, "signup_email", "TC04_duplicate_email")