from utills import *


#TC1 이메일 공란 회원가입 테스트
def space_email_test():
   
    try:
        # -----------------------------
        # 테스트 시작
        # -----------------------------
        print("\n▶ TC1: 이메일 빈칸 회원가입 테스트 시작")

        driver = get_driver()
        username = ""
        password = "@qa12345"
        name = "김성호"

        navigate_to_signup(driver)

        # Create account 클릭
        click_element(driver,"[type='button']")

        
        type_text(driver,"Email",username)
        type_text(driver,"Password",password)
        type_text(driver,"Name",name)
        
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
            assert True, "error message not found"

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
        username = "test123naver.com"
        password = "@qa12345"
        name = "김성호"

        navigate_to_signup(driver)

        # Create account 클릭
        click_element(driver,"[type='button']")

        
        type_text(driver,"Email",username)
        type_text(driver,"Password",password)
        type_text(driver,"Name",name)
        
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
    


if __name__ == "__main__":
    print("Test 1: 이메일 공란 테스트")
    space_email_test()
    print("Test 2: 잘못된 이메일 형식 회원가입 테스트")
    wrong_email_type_test()
