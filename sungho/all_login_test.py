from utills import *
from selenium.common.exceptions import TimeoutException



# tc1) 정상 로그인 → 로그아웃
def right_login():
    driver = get_driver()
    username = "qa3team03@elicer.com"
    password = "@qa12345"

    navigate_to_login(driver)

    print("\n▶ 가입된 계정 로그인 진행 중...")


    type_text(driver,"Email",username)
    type_text(driver,"Password",password)
    click_element(driver,"[type='submit']")
    time.sleep(2)


    # 로그인 후 화면에 나타나는 요소를 기다리기
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
    print("✔ 로그인 성공(메인 화면 로딩 확인됨)")
    logout(driver)
    driver.quit()

#tc2) 잘못된 비밀번호로 로그인 시도 테스트
def test_wrong_password():
    driver = get_driver()
    username = "qateam03@elicer.com"
    password = "!qa12345"
    navigate_to_login(driver)
    print("\n▶ 잘못된 비밀번호 테스트 시작")

    type_text(driver,"Email",username)
    type_text(driver,"Password",password)
    click_element(driver,"[type='submit']")
    time.sleep(2)
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
    username = "qateam03@alicer.com"
    password = "qa12345"
    navigate_to_login(driver)
    print("\n▶ 8글자 미만 비밀번호 테스트 시작")

    type_text(driver,"Email",username)
    type_text(driver,"Password",password)
    click_element(driver,"[type='submit']")
    time.sleep(2)

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
    username = "nonexist@alicer.com"
    password = "@qa12345"
    navigate_to_login(driver)
    
    print("\n▶ 미가입된 계정 로그인 테스트 시작")

    type_text(driver, "Email", username)
    type_text(driver, "Password", password)
    click_element(driver, "[type='submit']")
    time.sleep(2)

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
    test_wrong_password()
    print("Test 3: 8글자 미만 비밀번호 입력 테스트")
    short_password()
    print("Test 4: 미가입된 계정으로 로그인 테스트")
    nonexist_user_login()
    print("모든 로그인 테스트 종료!")

   
