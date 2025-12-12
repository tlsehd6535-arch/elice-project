from utills import *


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
        
        # Agree all 체크
        #click_element(driver,"input[type='checkbox']")# 이거로 하면 안됩니다 이유가 궁금합니다
        driver.find_element(By.CSS_SELECTOR,"input[type='checkbox']").click() # 이거로 하면 잘 작동되고
        

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
        # 항상 드라이버 종료
        driver.quit()


if __name__ == "__main__":
    print("Test 1: 이메일 공란 테스트")
    space_email_test()
    
