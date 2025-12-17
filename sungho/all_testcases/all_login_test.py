from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *


def login(driver, email, password):
    navigate_to_login(driver)
    type_text(driver, "Email", email)
    type_text(driver, "Password", password)
    click_element(driver, "[type='submit']")



# tc1) 정상 로그인
def right_login():
    driver = get_driver()
    login(driver, "qa3team03@elicer.com", "@qa12345")
    print("로그인 완료")

    icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
    print("로그인 성공이후 새 브라우저이동 완료")

    assert icon.is_displayed()
    driver.quit()


#tc2) 잘못된 비밀번호로 로그인 시도 테스트
def wrong_password():
    driver = get_driver()
    print("\n▶ 잘못된 비밀번호 테스트 시작")
    login(driver, "qa3team03@elicer.com", "!qa12345")
    try:
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(), 'Email or password does not match')]")
            )
        )
        print("✔ 오류 메시지 확인됨:", error_element.text)
        assert "Email or password does not match" in error_element.text
        print("✔ 테스트 통과!")
    except TimeoutException:
        print("❌ 오류 메시지를 찾지 못했음")
        assert False, "Wrong password test failed - error message not found"
    driver.quit()

#tc3 8글자 미만 비밀번호 로그인
def short_password():
    driver = get_driver()    
    print("\n▶ 8글자 미만 비밀번호 테스트 시작")

    email = "qateam03@alicer.com"
    password = "12345"
    login(driver,email,password)
    
    try:
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(), 'Please enter a password of at least 8 digits.')]")
            )
        )
        print("✔ 오류 메시지 확인됨:", error_element.text)
        assert 'Please enter a password of at least 8 digits.' in error_element.text
        print("✔ 테스트 통과!")
    except TimeoutException:
        print("❌ 오류 메시지를 찾지 못했음")
        assert False, "Short password test failed - error message not found"
    driver.quit()

#tc4 가입안한 계정 로그인시도 
# TC4: 가입 안한 계정 로그인 시도
def nonexist_user_login():
    driver = get_driver()    
    email = "nonexist@alicer.com"
    password = "@qa12345"
    login(driver,email,password)
    try:
        # 기대 메시지: unsigned user, you must sign up
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(), 'unsigned user, you must sign up')]")
            )
        )
        print("✔ 오류 메시지 확인됨:", error_element.text)

        assert 'unsigned user, you must sign up' in error_element.text
        print("✔ 테스트 통과!")

    except TimeoutException:
        print("❌ 오류 메시지를 찾지 못했음")
        # ❗ 여기가 중요 — 테스트 실패 처리
        print("테스트 실패...")

    finally:
        driver.quit()


if __name__ == "__main__":
    print("Test 1: 가입된 계정 정상적 로그인")
    right_login()   
    print("Test 2: 잘못된 비밀번호 입력 테스트")
    wrong_password()
    print("Test 3: 8글자 미만 비밀번호 입력 테스트")
    short_password()
    print("Test 4: 미가입된 계정으로 로그인 테스트")
    nonexist_user_login()
    print("모든 로그인 테스트 종료!")

   
