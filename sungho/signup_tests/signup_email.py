from utills import *
from selenium.common.exceptions import TimeoutException


#TC1 이메일 공란 회원가입 테스트
def space_email_test():
   
    try:
        # -----------------------------
        # 테스트 시작
        # -----------------------------
        print("\n▶ TC1: 이메일 빈칸 회원가입 테스트 시작")

        driver = get_driver()

        navigate_to_signup(driver)

        # Create account 클릭
        click_element(driver,"[type='button']")

        
        type_text(driver,"Email","")
        type_text(driver,"Password","@qa12345")
        type_text(driver,"Name","김성호")
        
        # 이용약관 Agree all 체크
        driver.find_element(By.CSS_SELECTOR,"input[type='checkbox']").click()
        

        # Create 버튼 클릭
        click_element(driver, "button[type='submit']")
    

        # HTML 기본 validation 메시지 읽기
        email_input = driver.find_element(By.XPATH, "//input[@placeholder='Email']")
        msg = driver.execute_script("return arguments[0].validationMessage;", email_input)

        print("브라우저 Validation Message:", msg)

        # -----------------------------
        # 커스텀 에러 메시지 검증
        # -----------------------------
        try:
            error_element = driver.find_element(By.XPATH, "//p[contains(text(), 'Please enter your email address')]")
            print("✔ 오류 메시지 확인됨:", error_element.text)
        except NoSuchElementException:
            print("❌ Please enter your email address 메시지를 찾지 못했음")
            

        print("✔ TC1 통과!")

    finally:
        
        driver.quit()
def wrong_email_type_test():
    try:
        # -----------------------------
        # 테스트 시작
        # -----------------------------
        print("\n▶ TC2: 잘못된 이메일 형식의 회원가입 테스트 시작")

        driver = get_driver()

        navigate_to_signup(driver)

        # Create account 클릭
        click_element(driver,"[type='button']")

        
        type_text(driver,"Email","test123naver.com")
        type_text(driver,"Password","@qa12345")
        type_text(driver,"Name","김성호")
        
        # 이용약관 Agree all 체크
        driver.find_element(By.CSS_SELECTOR,"input[type='checkbox']").click()
        

        # Create 버튼 클릭
        click_element(driver, "button[type='submit']")
    

        # HTML 기본 validation 메시지 읽기
        email_input = driver.find_element(By.XPATH, "//input[@placeholder='Email']")
        msg = driver.execute_script("return arguments[0].validationMessage;", email_input)

        print("브라우저 Validation Message:", msg)

        # -----------------------------
        # 커스텀 에러 메시지 검증
        # -----------------------------
        try:
            error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[contains(text(), 'Email address is incorrect.')]")))
            print("✔ 오류 메시지 확인됨:", error_element.text)
            assert "Email address is incorrect." in error_element.text
            print("✔ 테스트 통과!")
        except NoSuchElementException:
            print("❌ Please enter your email address 메시지를 찾지 못했음")
            assert False, "error message not found"

        print("✔ TC2 통과!")

    finally:
        driver.quit()

def right_signup_test():
    driver = get_driver()

    try:
        print("\n▶ TC3: 정상 회원가입 테스트 시작")

        username = generate_unique_username()  # ← 반드시 호출

        navigate_to_signup(driver)

        # Create account 클릭
        click_element(driver, "[type='button']")

        type_text(driver, "Email", username+"@naver.com")
        type_text(driver, "Password", "@qa12345")
        type_text(driver, "Name", "김성호")

        # 이용약관 Agree all 체크
        driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']").click()

        # Create 버튼 클릭
        click_element(driver, "button[type='submit']")
        

        # 회원가입 성공 화면 검증
        welcome_text = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(text(), 'Nice to meet you again')]")
            )
        )
        assert welcome_text.is_displayed()
        print("✔ 계정 정상적으로 생성")

        #생성된 계정으로 로그인 시도
        type_text(driver, "Password", "@qa12345")
        click_element(driver, "button[type='submit']")

        #ai-helpy-chat창으로 넘어가는지 시도
        try:
            WebDriverWait(driver, 10).until(
            EC.url_contains("/ai-helpy-chat")
        )
            print("✔ ai-helpy-chat 페이지 이동 확인 (테스트 성공)")
        except TimeoutException:
            print("❌ ai-helpy-chat 페이지로 이동하지 않음 (테스트 실패)")

    finally:
        driver.quit()

            
    


if __name__ == "__main__":
    print("Test 1: 이메일 공란 테스트")
    space_email_test()
    print("Test 2: 잘못된 이메일 형식 회원가입 테스트")
    wrong_email_type_test()
    print("Test3: 정상적 회원가입 후 로그인 테스트")
    right_signup_test()

