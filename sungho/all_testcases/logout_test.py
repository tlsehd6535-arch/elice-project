from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utills import *
from all_login_test import login

def login_logout():
    try:
         
        driver = get_driver()
        login(driver, "qa3team03@elicer.com", "@qa12345")
        print("로그인 완료")
        logout(driver)

        type_text(driver, "Password", "@qa12345")
        click_element(driver, "button[type='submit']")
        try: 
            WebDriverWait(driver, 15).until(
                EC.url_contains("/ai-helpy-chat")
            )
            icon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, '[data-testid="PersonIcon"]')
        )
    )
            assert icon.is_displayed()
            print("✔ ai-helpy-chat 페이지 이동 확인 (테스트 성공)")
        except TimeoutException:
            print("❌ ai-helpy-chat 페이지로 이동하지 않음 (테스트 실패)")
    finally:
        driver.quit()




if __name__ == "__main__":
    print("Test 17,18: 로그인-로그아웃 테스트")
    login_logout()   
