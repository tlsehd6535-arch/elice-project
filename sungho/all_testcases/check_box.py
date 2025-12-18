from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *

def checkbox_fill_signup(driver, email=None, password=None, name=None):
    if email is not None:
        type_text(driver, "Email", email)
    if password is not None:
        type_text(driver, "Password", password)
    if name is not None:
        type_text(driver, "Name", name)




def agree_all_check_test():
    try:
        print("TC11: agree all 체크하기")
        driver = get_driver()
        open_signup_page(driver)
        email = generate_unique_username()+"@naver.com"
        password = "@qa12345"
        name = "김성호"

        fill_signup_form(driver, email, password, name) #회원가입 입력필드에 이메일, 비번 ,이름 입력 후 전체 약관 click
        create_btn = WebDriverWait(driver,10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(), 'Create account')]")
            )
        )
        assert create_btn.is_displayed()
        print("Create account 활성화 되어있음")
        time.sleep(1)
    finally:
        driver.quit()

def required_option_unchecked_test():
    try:
        print("TC12: 필수 항목 미동의 시 가입 불가 ")
        driver = get_driver()
        open_signup_page(driver)
        email = generate_unique_username()+"@naver.com"
        password = "@qa12345"
        name = "김성호"
        checkbox_fill_signup(driver,email,password,name)
        age_checkbox = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//label[.//span[text()=\"I'm 14 years or older.\"]]")
            )
        )
        age_checkbox.click()
        time.sleep(1)

        optional_checkbox = WebDriverWait(driver,10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//label[.//span[text()='[Optional] Receive updates and promotional emails.']]")
            )
        )
        optional_checkbox.click()
        create_btn = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

        assert not create_btn.is_enabled()
        print("Create account 비활성화 확인")
        time.sleep(1)
    finally:
        driver.quit()
        

        



        
if __name__== "__main__":
    print("TC11: 이용약관 모두 체크 테스트")
    agree_all_check_test()
    print("\nTC12: 필수 항목 미동의 테스트")
    required_option_unchecked_test()



